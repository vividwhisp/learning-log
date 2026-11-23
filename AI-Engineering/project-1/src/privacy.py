import re
#A note about the first version: these are deliberately basic patterns for learning. They are not comprehensive detectors or proof that a document contains no sensitive information.

PATTERNS = {
    "email" : re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),
    "phone": re.compile(
        r"(?<!\w)(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\w)"
    ),
    "aadhaar_like": re.compile(
        r"(?<!\d)\d{4}[\s-]?\d{4}[\s-]?\d{4}(?!\d)"
    ),
    "pan_like": re.compile(
        r"\b[A-Z]{5}\d{4}[A-Z]\b"
    ),
    "api_key": re.compile(
        r"\b(?:sk-[A-Za-z0-9_-]{16,}|"
        r"gsk_[A-Za-z0-9_-]{16,}|"
        r"ghp_[A-Za-z0-9]{20,})\b"
    ),
    "password_or_secret": re.compile(
        r"\b(password|passwd|secret|api_key|token)"
        r"\s*[:=]\s*[\"']?([^\s\"']+)",
        re.IGNORECASE,
    ),
}

def scan_text(text: str) -> dict[str, int]:
    """Return counts of detected sensitive values, not the values themselves"""
    findings = {}

    for category, pattern in PATTERNS.items():
        matches = pattern.findall(text)
        if matches:
            findings[category] = len(matches)
    return findings

def redact_text(text: str) -> str:
    """Replace detected sensitive values with
    category placeholders"""

    redacted = text

    for category, pattern in PATTERNS.items():
        redacted = pattern.sub(
            f"[REDACTED_{category.upper()}]",
            redacted,
        )
    return redacted

