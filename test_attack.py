import pytest
import requests
import json
import os

def load_payloads():
    if os.path.exists('temp_payloads.json'):
        with open('temp_payloads.json', 'r') as f:
            return json.load(f)
    return []

@pytest.mark.parametrize("payload_data", load_payloads())
def test_vulnerability_payload(payload_data):
    """
    Tests if a payload successfully exploits the target.
    """
    payload = payload_data.get('payload_suggestion')
    v_type = payload_data.get('vulnerability_type')
    
    target_url = "http://127.0.0.1:5000"
    
    if "SQL" in v_type.upper():
        url = f"{target_url}/login"
        response = requests.get(url, params={"username": payload})
    elif "COMMAND" in v_type.upper():
        url = f"{target_url}/execute"
        response = requests.get(url, params={"cmd": payload})
    else:
        pytest.skip(f"Unsupported vulnerability type for automated test: {v_type}")

    # Success criteria: 200 OK and indications of sensitive data or successful execution
    assert response.status_code == 200
    
    # Check for successful exfiltration patterns
    # (Simplified: in SQL Injection, success might mean getting 'admin' data)
    success_indicators = ["admin", "supersecret", "root", "uid=", "total"]
    found_indicator = any(indicator in response.text.lower() for indicator in success_indicators)
    
    assert found_indicator, "Attack sent but no proof of exploit found in response."
