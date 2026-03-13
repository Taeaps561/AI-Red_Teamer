import subprocess
import time
import requests
import json
import os
import sys


class AttackVerifier:
    def __init__(self, target_url="http://127.0.0.1:5000"):
        self.target_url = target_url
        self.server_process = None

    def start_mock_server(self):
        """Starts the vulnerable Flask app in the background."""
        print("Starting mock vulnerable server...")
        self.server_process = subprocess.Popen(['python', 'app_vulnerable.py'])
        time.sleep(2)  # Give server time to start

    def stop_mock_server(self):
        """Stops the mock server."""
        if self.server_process:
            print("Stopping mock server...")
            self.server_process.terminate()

    def run_tests(self, payloads):
        """
        Runs pytest with the provided payloads.
        Saves payloads to a temporary file for pytest to read.
        """
        with open('temp_payloads.json', 'w', encoding='utf-8') as f:
            json.dump(payloads, f)

        print("Running automated attack verification...")
        # Use pytest to run the verification
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', 'test_attack.py', '--json-report', '--json-report-file=report.json'],
            capture_output=True, text=True
        )
        
        return self.parse_report()

    def parse_report(self):
        if os.path.exists('report.json'):
            with open('report.json', 'r') as f:
                return json.load(f)
        return None

    def generate_markdown_report(self, ai_results, test_results):
        """Generates the security_report.md content."""
        report = "# AI Red Team Security Report\n\n"
        report += "## Summary of AI Findings\n"
        
        for res in ai_results:
            report += f"### {res.get('vulnerability_type')} ({res.get('risk_level')})\n"
            report += f"- **Payload Suggestion**: `{res.get('payload_suggestion')}`\n"
            report += f"- **Remediation**: {res.get('remediation_guidance')}\n\n"

        report += "## Attack Verification Results\n"
        if test_results and 'tests' in test_results:
            for test in test_results['tests']:
                status = "✅ SUCCESS (Vulnerability Confirmed)" if test['outcome'] == 'passed' else "❌ FAILED (False Positive or No Exploit)"
                report += f"### Test: {test['nodeid']}\n"
                report += f"- **Result**: {status}\n"
        else:
            report += "No verification tests were executed.\n"
            
        return report
