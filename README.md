# VULNETT SECURITY ENGINE
### Autonomous Digital Intelligence & Perimeter Audit

<p align="center">
  <img src="https://img.icons8.com/fluency/96/security-checked.png" width="60"/>
</p>

**Vulnett** is a premium, autonomous security orchestration engine designed to identify network exposures, service misconfigurations, and active vulnerability signatures across digital perimeters. Built for security professionals, it combines high-performance network discovery with advanced threat intelligence.

---

## 🚀 Key Features

<p>
  <img src="https://img.icons8.com/ios-filled/50/network.png" width="18"/> 
  <b>Autonomous Reconnaissance</b><br>
  Orchestrates <code>nmap</code> for high-precision service identification and OS fingerprinting.
</p>

<p>
  <img src="https://img.icons8.com/ios-filled/50/artificial-intelligence.png" width="18"/> 
  <b>Intelligence Engine</b><br>
  Leverages <code>nuclei</code> for signature-based scanning against 5000+ CVEs and misconfigurations.
</p>

<p>
  <img src="https://img.icons8.com/ios-filled/50/combo-chart.png" width="18"/> 
  <b>Strategic Dashboard</b><br>
  Real-time interface with threat matrices, risk scoring, and infrastructure mapping.
</p>

<p>
  <img src="https://img.icons8.com/ios-filled/50/document.png" width="18"/> 
  <b>Executive Reports</b><br>
  Generates audit-ready PDF reports with clean, professional formatting.
</p>

<p>
  <img src="https://img.icons8.com/ios-filled/50/laptop.png" width="18"/> 
  <b>Cross-Platform</b><br>
  Seamless deployment across Windows and Linux.
</p>

<p>
  <img src="https://img.icons8.com/ios-filled/50/lock.png" width="18"/> 
  <b>Secure Gateway</b><br>
  Integrated <code>ngrok</code> support for encrypted remote access.
</p>

---

## 🛠️ Deployment

### Windows
```bash
setup.bat
run_scanner.bat
Linux
chmod +x setup.sh
./setup.sh

source .venv/bin/activate
python3 scanner.py
📈 Methodology
<p align="center"> <img src="https://img.icons8.com/ios/50/flow-chart.png" width="40"/> </p>

Vulnett follows a Non-Intrusive Metadata Aggregation model — analyzing service banners, headers, and public signatures without executing destructive payloads.

Standards: OWASP ASVS, NIST CSF, ISO 27001

Risk Model: Based on vulnerability density and service criticality

🏗️ Architecture

scanner.py — Core engine & Flask orchestration

setup.ps1 / setup.sh — Environment setup

static / templates — UI layer

requirements.txt — Dependencies

🧩 Requirements

Python 3.8+

Nmap

Nuclei

Internet access (for templates & ngrok)

⚠️ Disclaimer

Authorized security auditing only. Unauthorized use is strictly prohibited.

<p> align="center"> <b>© 2026 Vulnett Security Systems</b><br> Enterprise-grade security. Minimal. Precise. </p> ```
