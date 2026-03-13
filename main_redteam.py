import os
import sys
import scanner_engine
from attack_verifier import AttackVerifier

def main():
    print("--- AI-Red Teamer Starting ---")
    
    # Retrieve tokens from environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not github_token:
        print("Error: GITHUB_TOKEN is not set.")
        sys.exit(1)
    if not openai_api_key:
        print("Error: OPENAI_API_KEY is not set.")
        sys.exit(1)

    print("Tokens found. Starting security scan...")

    # 1. Read source code from latest commit
    code_snippets = scanner_engine.read_source_code()
    
    if not code_snippets:
        print("No .py or .js files modified in the latest commit. Skipping scan.")
        sys.exit(0)

    ai_results = []

    # 2. Analyze each file with AI
    for file_path, content in code_snippets.items():
        print(f"Analyzing {file_path}...")
        result = scanner_engine.analyze_with_ai(content)
        if result:
            ai_results.append(result)

    if not ai_results:
        print("No vulnerabilities detected by AI.")
        sys.exit(0)

    # 3. Automated Attack Verification
    verifier = AttackVerifier()
    verifier.start_mock_server()
    
    try:
        test_results = verifier.run_tests(ai_results)
        
        # 4. Generate Security Report
        report_content = verifier.generate_markdown_report(ai_results, test_results)
        with open('security_report.md', 'w', encoding='utf-8') as f:
            f.write(report_content)
        print("\nSecurity report generated: security_report.md")

        # 5. Handle exit logic
        found_high_risk = any(res.get('risk_level') == 'High' for res in ai_results)
        if found_high_risk:
            print("\nCRITICAL: One or more high-risk vulnerabilities detected! Stopping pipeline.")
            sys.exit(1)
        else:
            print("\nScan completed. No high-risk vulnerabilities found.")
            sys.exit(0)

    finally:
        verifier.stop_mock_server()

if __name__ == "__main__":
    main()
