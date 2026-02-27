# <img src="./static/logo.png" width="40" height="40" valign="middle"> VULNETT SECURITY ENGINE
### *Autonomous Perimeter Intelligence & Strategic Audit*

[![Python](https://img.shields.io/badge/Python-3.9+-007aff?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Nmap](https://img.shields.io/badge/Orchestrator-Nmap-007aff?style=for-the-badge&logo=nmap&logoColor=white)](https://nmap.org)
[![Nuclei](https://img.shields.io/badge/Vuln--Engine-Nuclei-007aff?style=for-the-badge&logo=discovery&logoColor=white)](https://projectdiscovery.io)
[![License](https://img.shields.io/badge/License-MIT-34c759?style=for-the-badge)](LICENSE)

**Vulnett** is a portable, high-fidelity security orchestration engine built for automated surface audits. It combines the raw power of **Nmap** for service discovery with the intelligence of **Nuclei** for signature-based scanning, all wrapped in a premium, glassmorphic web dashboard.

---

## 📸 Interface Preview

<p align="center">
  <img src="./static/logo.png" width="300" alt="Vulnett Logo">
  <br>
  <i>Designed for the modern security researcher. One-click from audit to intelligence.</i>
</p>

---

## 🌟 Core Capabilities

*   **🛡️ Autonomous Reconnaissance**: High-precision service identification and OS fingerprinting using optimized Nmap profiles.
*   **🧠 Logic-Based Auditing**: Correlates 5000+ Nuclei signatures to identify CVEs, misconfigurations, and standard exposures.
*   **📊 Strategic Analytics**: A real-time, premium web dashboard featuring threat matrices, risk index scoring, and infrastructure mapping.
*   **📄 Executive Reporting**: Generates audit-ready PDF reports with high-end typography and compliance-ready formatting.
*   **☁️ Edge Gateway**: Integrated with `ngrok` for secure, encrypted cloud tunneling of local audit dashboards.
*   **📦 Zero-Config Portability**: Designed to be truly "unzip-and-run" with platform-specific auto-installers.

---

## 🛠️ System Requirements

| Tool | Purpose | Status |
| :--- | :--- | :--- |
| **Python 3.9+** | Execution Logic | Essential |
| **Nmap** | Network Discovery | Integrated / Auto-installed |
| **Nuclei** | Vulnerability Intel | Integrated / Auto-installed |
| **Ngrok** | Cloud Tunneling | Optional |

---

## 🚀 Rapid Deployment

### 🪟 Windows (Recommended)
Vulnett provides a seamless one-click experience for Windows using powershell-backed batch files.

1.  **Clone/Download** the repository.
2.  Double-click **`setup.bat`** (Automatically installs Nmap/Nuclei & Dependencies).
3.  Double-click **`run_scanner.bat`** to launch the Intelligence Gateway.

### 🐧 Linux (Manual)
```bash
# Initialize high-performance environment
chmod +x setup.sh
./setup.sh

# Activate and launch
source .venv/bin/activate
python3 scanner.py
```

---

## 📈 Methodology
Vulnett operates on a **Non-Intrusive Metadata Aggregation** model. It performs:
1.  **Service Inventory**: Probing the top-100 most critical ports.
2.  **Product Fingerprinting**: Identifying versions of web servers, databases, and services.
3.  **Signature Matching**: Mapping identified services against known vulnerability databases.
4.  **Risk Quantification**: Calculating a normalized security score (0-100) based on severity density.

---

## 📄 Compliance Alignment
Vulnett findings are mapped against globally recognized security frameworks to ensure audit readiness:
- **OWASP ASVS** (Application Security Verification Standard)
- **NIST CSF** (Cybersecurity Framework)
- **ISO 27001** (Information Security Management)

---

## ⚠️ Disclaimer
*This tool is intended for authorized security auditing and educational purposes only. Unauthorized scanning of networks without prior written permission is illegal.*

&copy; 2026 VULNETT SECURITY SYSTEMS. PREMIUM DIGITAL DEFENSE.
