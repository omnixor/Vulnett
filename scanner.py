import subprocess
import xml.etree.ElementTree as ET
import json
import sys
import os
from datetime import datetime
from flask import Flask, render_template, send_file, request, redirect, url_for
from pyngrok import ngrok
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import shutil
import platform
import socket

# Configuration
PORT = 5001
MAX_PORT_ATTEMPTS = 10
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
REPORT_DIR = os.path.join(BASE_DIR, 'reports')

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)

# Global State
CURRENT_TARGET = "scanme.nmap.org"
PUBLIC_URL = ""

# Ensure directories exist
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATE_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# ---------------- CORE LOGIC ----------------

def run_nmap(target):
    print(f"[*] Analyzing network perimeter: {target}")
    # standard scan for better coverage
    # Using more flags for service detection and OS fingerprinting
    subprocess.run(["nmap", "-sV", "-T4", "--top-ports", "100", "-oX", "scan.xml", target], capture_output=True)

def parse_nmap():
    if not os.path.exists("scan.xml"): return []
    try:
        tree = ET.parse("scan.xml")
        root = tree.getroot()
        results = []
        for port in root.findall('.//port'):
            state_node = port.find('state')
            if state_node is not None and state_node.get('state') == 'open':
                service_node = port.find('service')
                results.append({
                    "port": port.get('portid'),
                    "service": service_node.get('name') if service_node is not None else "unknown",
                    "product": service_node.get('product') if service_node is not None else "",
                    "version": service_node.get('version') if service_node is not None else ""
                })
        return results
    except Exception as e:
        print(f"[!] Nmap parse error: {e}")
        return []

def run_nuclei(target):
    print(f"[*] Probing for vulnerabilities...")
    # Added filters for speed and severity
    subprocess.run(["nuclei", "-u", target, "-jsonl", "-o", "nuclei.json", "-ni", "-silent"], capture_output=True)

def parse_nuclei():
    findings = []
    if not os.path.exists("nuclei.json"): return []
    try:
        with open("nuclei.json") as f:
            for line in f:
                if not line.strip(): continue
                data = json.loads(line)
                findings.append({
                    "name": data.get("info", {}).get("name") or data.get("template-id"),
                    "severity": data.get("info", {}).get("severity", "info").lower(),
                    "description": data.get("info", {}).get("description", "No description provided."),
                    "reference": data.get("info", {}).get("reference", []),
                    "host": data.get("host"),
                    "matched": data.get("matched-at")
                })
    except Exception as e:
        print(f"[!] Nuclei parse error: {e}")
    return findings

# ---------------- UTILS ----------------

def find_available_port(start_port, max_attempts=MAX_PORT_ATTEMPTS):
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except socket.error:
                continue
    return start_port 

def get_stats(findings):
    stats = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        sev = f["severity"]
        if sev in stats:
            stats[sev] += 1
    return stats

def calculate_score(findings):
    weights = {"critical": 10, "high": 7, "medium": 4, "low": 2, "info": 0.5}
    total_score = sum(weights.get(f["severity"], 0) for f in findings)
    normalized = min(total_score * 5, 100) 
    level = "Critical" if normalized >= 70 else "High" if normalized >= 40 else "Medium" if normalized >= 15 else "Low"
    return round(normalized, 1), level

# ---------------- PDF GENERATOR ----------------

class VulnettReport:
    def __init__(self, filename, target, ports, findings, score, level, stats):
        self.filename = filename
        self.target = target
        self.ports = ports
        self.findings = findings
        self.score = score
        self.level = level
        self.stats = stats
        self.styles = getSampleStyleSheet()
        self.logo_path = os.path.join(STATIC_DIR, 'logo.png')
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        # Premium Typography
        self.styles.add(ParagraphStyle(
            name='VulnettHeader',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor("#1d1d1f"),
            fontName='Helvetica-Bold',
            spaceAfter=10
        ))
        self.styles.add(ParagraphStyle(
            name='VulnettSubHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor("#007aff"),
            fontName='Helvetica-Bold',
            spaceAfter=20
        ))
        self.styles.add(ParagraphStyle(
            name='StandardBody',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#3a3a3c"),
            fontName='Helvetica'
        ))
        self.styles.add(ParagraphStyle(
            name='FindingTitle',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#1d1d1f"),
            fontName='Helvetica-Bold',
            spaceBefore=10
        ))

    def generate(self):
        doc = SimpleDocTemplate(
            self.filename,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        elements = []

        # 1. Header with Logo
        if os.path.exists(self.logo_path):
            logo = Image(self.logo_path, 1.8*inch, 0.5*inch)
            logo.hAlign = 'LEFT'
            elements.append(logo)
        else:
            elements.append(Paragraph("VULNETT SECURITY", self.styles['VulnettHeader']))
        
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"Autonomous Security Intelligence Report", self.styles['VulnettSubHeader']))
        elements.append(Paragraph(f"<b>Target Scope:</b> {self.target}", self.styles['StandardBody']))
        elements.append(Paragraph(f"<b>Audit Timestamp:</b> {datetime.now().strftime('%B %d, %Y | %H:%M UTC')}", self.styles['StandardBody']))
        elements.append(Spacer(1, 30))

        # 2. Executive Summary / Risk Score
        elements.append(Paragraph("I. SECURITY POSTURE SUMMARY", self.styles['Heading3']))
        
        score_color = colors.red if self.score > 50 else colors.orange if self.score > 20 else colors.green
        
        summary_data = [
            ["Risk Index Score", f"{self.score} / 100"],
            ["Threat Classification", self.level.upper()],
            ["Infrastucture Status", "MODERATE RISK" if self.score > 20 else "STABLE"]
        ]
        t_summary = Table(summary_data, colWidths=[2.5*inch, 3.5*inch])
        t_summary.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 11),
            ('TEXTCOLOR', (1,0), (1,0), score_color),
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#f5f5f7")),
            ('GRID', (0,0), (-1,-1), 1, colors.whitesmoke),
            ('PADDING', (0,0), (-1,-1), 12),
        ]))
        elements.append(t_summary)
        elements.append(Spacer(1, 25))

        # 3. Port Inventory
        elements.append(Paragraph("II. PERIMETER SERVICE INVENTORY", self.styles['Heading3']))
        port_list = [["Port", "Service", "Version / Product Fingerprint"]]
        for p in self.ports:
            product_info = f"{p.get('product', '')} {p.get('version', '')}".strip() or "General Service"
            port_list.append([p['port'], p['service'].upper(), product_info])
        
        if not self.ports:
            port_list.append(["N/A", "N/A", "No open ports identified in standard top-100 scan."])

        tp = Table(port_list, colWidths=[1*inch, 1.5*inch, 3.5*inch], repeatRows=1)
        tp.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#007aff")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        elements.append(tp)
        elements.append(Spacer(1, 25))

        # 4. Findings
        elements.append(Paragraph("III. VULNERABILITY INTELLIGENCE", self.styles['Heading3']))
        if self.findings:
            for f in self.findings:
                elements.append(Paragraph(f.get('name', 'Unknown Vulnerability'), self.styles['FindingTitle']))
                
                sev_color = self._get_severity_color(f['severity'])
                elements.append(Paragraph(
                    f"Severity: <font color='{sev_color}'><b>{f['severity'].upper()}</b></font> | Impacting: {f.get('host', 'N/A')}",
                    self.styles['StandardBody']
                ))
                
                desc = f.get('description', 'Detailed analysis restricted.')
                elements.append(Paragraph(f"<b>Discovery Logic:</b> {desc}", self.styles['StandardBody']))
                
                if f.get('reference'):
                    refs = f['reference'] if isinstance(f['reference'], list) else [f['reference']]
                    elements.append(Paragraph(f"<b>Intel Sources:</b> {', '.join(refs[:2])}", self.styles['StandardBody']))
                
                elements.append(Spacer(1, 8))
        else:
            elements.append(Paragraph("Evaluation complete: No deterministic vulnerabilities identified at the current maturity level. The target shows high resistance to standard scanning patterns.", self.styles['StandardBody']))
        
        # 5. Methodology
        elements.append(Spacer(1, 40))
        elements.append(Paragraph("IV. AUDIT SCOPE & COMPLIANCE", self.styles['Heading3']))
        elements.append(Paragraph(
            "The data contained in this report is produced by the Vulnett Autonomous Security Engine. The methodology "
            "includes metadata aggregation from public network nodes and signature-based pattern matching. "
            "Note: This is an external security assessment and does not constitute a full-scope penetration test.",
            self.styles['StandardBody']
        ))

        doc.build(elements)

    def _get_severity_color(self, severity):
        colors_map = {
            "critical": colors.red,
            "high": colors.darkorange,
            "medium": colors.gold,
            "low": colors.green,
            "info": colors.blue
        }
        return colors_map.get(severity.lower(), colors.black)

# ---------------- ROUTES ----------------

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/initiate_scan", methods=["POST"])
def initiate_scan():
    global CURRENT_TARGET
    target = request.form.get("target")
    if not target: return redirect(url_for("landing"))
    
    # Sanitize target (very basic)
    target = target.replace("http://", "").replace("https://", "").split("/")[0]
    CURRENT_TARGET = target
    
    # Clean up previous results
    if os.path.exists("scan.xml"): os.remove("scan.xml")
    if os.path.exists("nuclei.json"): os.remove("nuclei.json")
    
    # Execute Scan
    run_nmap(CURRENT_TARGET)
    run_nuclei(CURRENT_TARGET)
    
    link = PUBLIC_URL if PUBLIC_URL else f"http://127.0.0.1:{PORT}"
    dashboard_url = f"{link}/dashboard"
    
    return render_template("success.html", url=dashboard_url, target=CURRENT_TARGET)

@app.route("/dashboard")
def dashboard():
    ports = parse_nmap()
    findings = parse_nuclei()
    stats = get_stats(findings)
    score, level = calculate_score(findings)
    
    return render_template("index.html", 
                         target=CURRENT_TARGET, 
                         ports=ports, 
                         findings=findings, 
                         score=score, 
                         level=level, 
                         stats=stats, 
                         timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route("/download")
def download():
    ports = parse_nmap()
    findings = parse_nuclei()
    stats = get_stats(findings)
    score, level = calculate_score(findings)
    
    # Generate in reports folder
    report_name = f"Vulnett_Report_{CURRENT_TARGET}.pdf"
    report_path = os.path.join(REPORT_DIR, report_name)
    
    rep = VulnettReport(report_path, CURRENT_TARGET, ports, findings, score, level, stats)
    rep.generate()
    
    return send_file(report_path, mimetype='application/pdf', as_attachment=True, download_name=report_name)

# ---------------- MAIN ----------------

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 VULNETT SECURITY ENGINE - NEXUS GATEWAY ACTIVE")
    print("="*50)
    
    # Dynamic Port Selection
    original_port = PORT
    PORT = find_available_port(original_port)
    if PORT != original_port:
        print(f"[!] PORT {original_port} IN USE. Dynamically routed to: {PORT}")
    
    # Check for System Dependencies
    missing = []
    if not shutil.which("nmap"): missing.append("nmap")
    if not shutil.which("nuclei"): missing.append("nuclei")
    
    if missing:
        print(f"❌ CRITICAL: Missing tools: {', '.join(missing)}")
        if platform.system() == "Windows":
            print("Action: Run 'setup.bat' as Administrator.")
        else:
            print("Action: Run './setup.sh'.")
        sys.exit(1)

    # Tunnel Initialization (Robust)
    try:
        # Check if ngrok is configured
        tunn = ngrok.connect(PORT)
        PUBLIC_URL = tunn.public_url
        print(f"\n[+] CLOUD GATEWAY: {PUBLIC_URL}")
    except Exception as e:
        print(f"\n[!] CLOUD TUNNEL: Local mode only (Ngrok not configured or limited).")
        print(f"[+] LOCAL ACCESS: http://127.0.0.1:{PORT}")

    app.run(port=PORT, debug=False)

