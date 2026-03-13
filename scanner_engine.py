import os
import subprocess
import json
from openai import OpenAI

def read_source_code():
    """
    Reads .py and .js files modified in the latest commit.
    """
    print("Reading source code from latest commit...")
    try:
        # Get names of files changed in the last commit
        result = subprocess.run(
            ['git', 'show', '--name-only', '--pretty=format:'],
            capture_output=True, text=True, check=True
        )
        files = result.stdout.split('\n')
        
        target_files = [f for f in files if f.endswith(('.py', '.js'))]
        
        code_snippets = {}
        for file_path in target_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    code_snippets[file_path] = f.read()
        
        return code_snippets
    except Exception as e:
        print(f"Error reading git commit: {e}")
        return {}

def analyze_with_ai(code_snippet):
    """
    Sends code to local Ollama (llama3.2) for vulnerability analysis.
    """
    # Ollama has an OpenAI-compatible endpoint at localhost:11434
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama" # api_key is required but ignored by Ollama
    )
    
    system_prompt = (
        "You are a Red Team Lead. Your task is to identify OWASP Top 10 vulnerabilities in this code "
        "and create a sample Proof of Concept (PoC) payload. "
        "Respond ONLY in JSON format with fields: vulnerability_type, risk_level (Low/Med/High), "
        "payload_suggestion, and remediation_guidance"
    )
    
    try:
        response = client.chat.completions.create(
            model="llama3.2",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this code:\n\n{code_snippet}"}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error during AI analysis: {e}")
        return None
