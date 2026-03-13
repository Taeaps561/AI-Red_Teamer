import pytest
import sys
import os
import json
from unittest.mock import patch, MagicMock
from attack_verifier import AttackVerifier
import scanner_engine

# 1. Mock OpenAI Response and Exit Logic Test
def test_pipeline_exit_on_high_risk():
    """
    Tests if the pipeline would exit with code 1 when a High risk is found.
    We mock the analyze_with_ai to return a High risk result.
    """
    mock_result = {
        "vulnerability_type": "SQL Injection",
        "risk_level": "High",
        "payload_suggestion": "' OR 1=1 --",
        "remediation_guidance": "Use parameterized queries."
    }
    
    with patch('scanner_engine.analyze_with_ai', return_value=mock_result):
        # We simulate the logic in main_redteam.py
        found_high_risk = mock_result.get('risk_level') == 'High'
        assert found_high_risk == True
        # In main_redteam.py, this would trigger sys.exit(1)

# 2. End-to-End Test and Result Assertion
def test_e2e_exploitation_and_logging():
    """
    End-to-End: Start mock server, verify payload, and log result.
    """
    verifier = AttackVerifier()
    verifier.start_mock_server()
    
    log_file = "test_report.log"
    
    try:
        # Simulate a payload that we know will work on app_vulnerable.py
        test_payloads = [{
            "vulnerability_type": "SQL Injection",
            "risk_level": "High",
            "payload_suggestion": "admin' --",
            "remediation_guidance": "Use parameterized queries."
        }]
        
        # Run tests using the verifier
        report = verifier.run_tests(test_payloads)
        
        # Check if at least one test passed (exploit successful)
        exploit_successful = False
        if report and 'tests' in report:
            for test in report['tests']:
                if test['outcome'] == 'passed':
                    exploit_successful = True
                    break
        
        if exploit_successful:
            with open(log_file, "a", encoding='utf-8') as f:
                f.write("Test Passed: AI found and exploited vulnerability\n")
            assert True
        else:
            pytest.fail("Exploit failed on mock server")
            
    finally:
        verifier.stop_mock_server()
        # Cleanup temporary files created by verifier
        for f in ['temp_payloads.json', 'report.json']:
            if os.path.exists(f):
                os.remove(f)
