# 🔴 AI-Red Teamer

> Local AI-powered security scanner that thinks like an attacker — detecting OWASP Top 10 vulnerabilities before they reach production.

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-llama3.2-black?logo=ollama&logoColor=white)](https://ollama.com/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![OWASP](https://img.shields.io/badge/Coverage-OWASP%20Top%2010-red)](https://owasp.org/www-project-top-ten/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Run a Local Scan](#run-a-local-scan)
- [CI/CD Integration](#cicd-integration)
  - [GitHub Actions Setup](#github-actions-setup)
  - [Required Secrets](#required-secrets)
- [Output](#output)
- [Project Structure](#project-structure)
- [References / Useful Resources](#references--useful-resources)
- [My Notes](#my-notes)

---

## Overview

**AI-Red Teamer** is a local-first automated security scanner that combines **Static Code Analysis** with **Exploit Simulation** — powered entirely by a locally-hosted LLM (Llama 3.2 via Ollama).

Unlike traditional SAST tools, AI-Red Teamer doesn't just flag suspicious patterns. It goes further by generating real attack payloads and verifying them against a sandboxed Mock Server — confirming whether a vulnerability is actually exploitable before reporting it.

All analysis stays on your machine. **No code is ever sent to the cloud.**

> 📦 Open-source | `ai-red-teamer`
> 🎯 Covers OWASP Top 10 vulnerability categories

  <img src="assets/images/screenshot.png" width="800" alt="AI-Red Teamer Screenshot"/>

---

## Key Features

| Feature | Description |
|---|---|
| 🤖 AI-Driven Analysis | Uses Ollama (llama3.2) locally — fully private, no cloud dependency |
| 💥 Exploit Simulation | Generates real payloads and verifies them via Pytest against a Mock Server |
| 🚦 CI/CD Integration | GitHub Actions integration with automatic pipeline halt on High-risk findings |
| 📋 Security Report | Auto-generates `security_report.md` with findings and remediation guidance |
| 🔒 Privacy-First | Zero code exfiltration — all LLM inference runs on local hardware |
| 🔄 Incremental Scanning | Scanner engine detects and targets only modified files for efficiency |

---

## System Architecture

The system is composed of 4 coordinated components:

```
  Source Code (Modified Files)
          │
          ▼
┌─────────────────────────┐
│   1. Scanner Engine     │  Detects changed files → sends to Local AI (Ollama)
│      scanner_engine.py  │  Identifies potential OWASP Top 10 vulnerabilities
└────────────┬────────────┘
             │ Vulnerability + Payload
             ▼
┌─────────────────────────┐     ┌──────────────────────────┐
│   2. Attack Verifier    │────▶│   3. Mock Engine          │
│      attack_verifier.py │     │      mock_server.py       │
│   Executes payloads via │     │   Sandboxed server with   │
│   Pytest exploit tests  │◀────│   intentional vuln targets│
└────────────┬────────────┘     └──────────────────────────┘
             │ Verified Results
             ▼
┌─────────────────────────┐
│   4. Orchestrator       │  Controls full flow + returns exit codes
│      main_redteam.py    │  Generates security_report.md
└────────────┬────────────┘
             │
        Pass │ Fail
        ┌────┴────┐
        ▼         ▼
    ✅ exit 0  ❌ exit 1
    Pipeline   Pipeline
    continues  blocked
```

### Component Responsibilities

- **`scanner_engine.py`** — Scans modified files and queries Ollama for vulnerability analysis and payload generation.
- **`attack_verifier.py`** — Takes AI-generated payloads and executes real exploit attempts against the Mock Engine using Pytest.
- **`mock_server.py`** — A sandboxed server with intentional vulnerabilities, serving as a safe exploit target.
- **`main_redteam.py`** — Orchestrator that controls the full scan-verify-report flow and returns CI/CD-compatible exit codes.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Local LLM | [Ollama](https://ollama.com/) + `llama3.2` |
| Exploit Testing | [Pytest](https://pytest.org/) |
| CI/CD | [GitHub Actions](https://github.com/features/actions) |
| Mock Server | Python (sandboxed vulnerable server) |
| Runtime | Python 3.10+ |
| Alternative LLM | OpenAI GPT-4o (optional, configurable) |

---

## Quick Start

### Prerequisites

- ✅ **Python 3.10+** installed
- ✅ **Ollama** installed and running locally
- ✅ `llama3.2` model pulled into Ollama

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Taeaps561/AI-Red_Teamer.git
cd ai-red-teamer

# 2. Install Python dependencies
pip install -r requirements.txt
```

### Setup Ollama

```bash
# Install Ollama (if not already installed)
# https://ollama.com/download

# Pull and run the required model
ollama run llama3.2
```

> ⚠️ **Note:** Keep `ollama run llama3.2` running in a separate terminal before starting the scanner.

---

### Run a Local Scan

```bash
# Run the full Red Team scan against your codebase
python main_redteam.py
```

```bash
# Run the exploit verification test suite independently
python -m pytest tests/test_redteam_logic.py
```

Results will be written to `security_report.md` in the project root.

---

## CI/CD Integration

### GitHub Actions Setup

AI-Red Teamer integrates natively with GitHub Actions. The orchestrator returns standard exit codes:

| Exit Code | Meaning | Pipeline Effect |
|---|---|---|
| `0` | No High/Critical findings | ✅ Pipeline continues |
| `1` | High or Critical vulnerability confirmed | ❌ Pipeline blocked |

Add the scanner as a step in your workflow:

```yaml
# .github/workflows/redteam.yml
name: AI Red Team Scan

on: [push, pull_request]

jobs:
  redteam:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run AI Red Team Scanner
        run: python main_redteam.py

      - name: Upload Security Report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: security-report
          path: security_report.md
```

---

### Required Secrets

Configure the following secrets in your GitHub repository settings:

| Secret | Required | Description |
|---|---|---|
| `GITHUB_TOKEN` | ✅ Yes | Auto-provided by GitHub Actions for pipeline integration |
| `OPENAI_API_KEY` | ⬜ Optional | Only needed if switching from Ollama to GPT-4o in `scanner_engine.py` |

---

## Output

After each scan, AI-Red Teamer generates a `security_report.md` containing:

- **Vulnerability summary** — list of confirmed findings with OWASP category
- **Severity rating** — Critical / High / Medium / Low per finding
- **Exploit evidence** — payload used and server response confirming exploitability
- **Remediation guidance** — actionable fix recommendations per vulnerability

---

## Project Structure

```
ai-red-teamer/
│
├── main_redteam.py           # Orchestrator — entry point
├── scanner_engine.py         # File scanner + Ollama AI analysis
├── attack_verifier.py        # Payload executor + exploit verifier
├── mock_server.py            # Sandboxed vulnerable server (test target)
├── requirements.txt
│
├── tests/
│   └── test_redteam_logic.py # Pytest exploit verification suite
│
└── security_report.md        # Auto-generated scan output (git-ignored)
```

---

## References / Useful Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Pytest Documentation](https://docs.pytest.org/)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [NIST Application Security Guidelines](https://csrc.nist.gov/)
- [GitHub Actions: Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)

---

## My Notes

> 📝 This project was built to explore the intersection of LLM-assisted reasoning and practical offensive security — specifically, whether a local model can reason about code vulnerabilities well enough to generate valid exploit payloads. The Mock Engine approach allows safe verification without touching production systems. Contributions welcome.

---

## License

MIT License. Created as part of the **AI-Red Teamer** security research portfolio.

---

*Think like an attacker. Defend like an engineer.*
