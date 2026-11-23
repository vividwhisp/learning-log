from src.privacy import scan_text, redact_text

def test_detects_sensitive_data():
    text = """
    Email: alice@example.com
    Phone: +91 98765 43210
    Aadhaar: 1234 5678 9012
    PAN: ABCDE1234F
    API key: sk-abcdefghijklmnop
    password=superpowert123
    """
    findings = scan_text(text)

    assert findings["email"] == 1
    assert findings["phone"] == 1
    assert findings["aadhaar_like"] == 1
    assert findings["pan_like"] == 1
    assert findings["api_key"] == 1
    assert findings["password_or_secret"] == 1

def test_redacts_sensitive_data():
    text = """
    Contact alice@example.com
    API key: sk-abcdefghijklmnop
    """

    redacted = redact_text(text)
    assert "alice@example.com" not in redacted
    assert "sk-abcdefghijklmnop" not in redacted
    assert "[REDACTED_EMAIL]" in redacted
    assert "[REDACTED_API_KEY]" in redacted

def test_preserves_normal_text():
    text = "Kubernetes is an open-source container orchestration platform."

    assert redact_text(text) == text
    assert scan_text(text) == {}


def test_scan_does_not_return_sensitive_values():
    text = "Email: alice@example.com"

    findings = scan_text(text)

    assert findings == {"email": 1}
    assert "alice@example.com" not in str(findings)
