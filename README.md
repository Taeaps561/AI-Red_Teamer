# AI-Red Teamer: Local AI-Powered Security Scanner

A smart security system using **Local LLM (Ollama)** to analyze code and simulate automated attacks (Automated Red Teaming) to detect OWASP Top 10 vulnerabilities before deployment.

## 🚀 Features
- **AI-Driven Analysis**: Uses Ollama (llama3.2) for privacy-first code analysis (no code sent to the cloud).
- **Automated Verification**: Confirms vulnerabilities by simulating real attacks (exploit simulation) via Pytest.
- **CI/CD Integration**: Supports GitHub Actions to immediately stop the pipeline upon detecting High-risk vulnerabilities.
- **Vulnerability Reporting**: Generates a `security_report.md` summary with remediation guidance.

## 🛠 System Architecture
The system consists of 4 main components:
1. **Scanner Engine**: Scans for modified files and sends them to the Local AI.
2. **Attack Verifier**: Takes payloads from the AI and attempts to exploit them against a Mock Server.
3. **Mock Engine**: A sandboxed server with intentional vulnerabilities for testing.
4. **Orchestrator**: Controls the entire flow and returns exit codes for CI/CD.

## 📦 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Ollama**:
   - Install [Ollama](https://ollama.com/)
   - Run the model: `ollama run llama3.2`

3. **Run Local Scan**:
   ```bash
   python main_redteam.py
   ```

4. **Run Full Test Suite**:
   ```bash
   python -m pytest tests/test_redteam_logic.py
   ```

## 🛡 GitHub Configuration
To use this in GitHub Actions, add the following Secrets:
- `GITHUB_TOKEN`: For integration authentication.
- `OPENAI_API_KEY`: (Optional) If you want to switch to GPT-4o instead of Ollama (adjustable in `scanner_engine.py`).

## 📄 License
MIT License
