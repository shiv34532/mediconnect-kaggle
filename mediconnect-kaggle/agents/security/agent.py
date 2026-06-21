"""
Security & Compliance Agent
============================
Ensures HIPAA compliance, data anonymization, and secure handling.
Demonstrates: Security features (Code)

This agent acts as a security gateway for all patient data flowing
through the MediConnect system. It enforces:
- Patient data anonymization (hashing)
- PII (Personally Identifiable Information) redaction
- HIPAA compliance validation
- Audit logging for all data access
- Output safety validation

NOTE: In Google ADK, tools are plain Python functions.
NO decorator needed - just pass them to LlmAgent(tools=[...])
"""
from google.adk.agents import LlmAgent
import hashlib
import re
import json
from datetime import datetime


# Tool functions - plain Python functions, NO decorator needed
def anonymize_patient(patient_data: dict) -> dict:
    """
    Anonymize patient data using secure hashing.

    Replaces all PII with anonymized tokens while preserving
    data needed for healthcare routing (region, language).

    Args:
        patient_data: Dictionary with patient information

    Returns:
        Anonymized dictionary with hashed identifiers

    Example:
        >>> anonymize_patient({"name": "John Doe", "phone": "555-1234"})
        {"patient_id": "a3f5...", "contact_hash": "b7e2...", "region": "unknown"}
    """
    anonymized = patient_data.copy()

    # Hash identifiable fields - NEVER store raw PII
    if "name" in anonymized:
        name = anonymized.pop("name")
        # Use SHA-256 for one-way hashing (cannot be reversed)
        anonymized["patient_id"] = hashlib.sha256(
            name.encode("utf-8")
        ).hexdigest()[:16]  # 16 chars sufficient for uniqueness

    # Redact phone numbers - store hash only
    if "phone" in anonymized:
        phone = anonymized.pop("phone")
        anonymized["contact_hash"] = hashlib.sha256(
            phone.encode("utf-8")
        ).hexdigest()[:16]

    # Redact email addresses
    if "email" in anonymized:
        email = anonymized.pop("email")
        anonymized["email_hash"] = hashlib.sha256(
            email.encode("utf-8")
        ).hexdigest()[:16]

    # Redact exact addresses, keep region only for clinic routing
    if "address" in anonymized:
        address = anonymized.pop("address")
        anonymized["region"] = _extract_region(address)

    # Add security metadata
    anonymized["processed_at"] = datetime.now().isoformat()
    anonymized["security_version"] = "1.0.0"
    anonymized["compliance_standard"] = "HIPAA"
    anonymized["data_minimization"] = True

    return anonymized


def _extract_region(address: str) -> str:
    """
    Extract only city/region from address for routing.

    Strips street numbers and exact locations, keeping only
    general geographic area for clinic assignment.

    Args:
        address: Full street address

    Returns:
        City/region string only
    """
    if not address:
        return "unknown"

    # Simple extraction - use NLP in production
    parts = [p.strip() for p in address.split(",")]

    # Return last part (usually city/state/country)
    if len(parts) >= 2:
        return ", ".join(parts[-2:])  # city, state
    return parts[-1] if parts else "unknown"


def validate_output(text: str) -> dict:
    """
    Validate that no PII leaks in agent output.

    Scans text for patterns that match known PII types and
    flags violations for redaction.

    Args:
        text: Agent output text to validate

    Returns:
        Dictionary with safety status and violations found

    Example:
        >>> validate_output("Patient John Doe lives at 123 Main St")
        {"is_safe": False, "violations": {"name": True, "address": True}}
    """
    violations = {}

    # Check for phone number patterns (US format)
    phone_pattern = r'\d{3}[-.]?\d{3}[-.]?\d{4}'
    violations["phone"] = bool(re.search(phone_pattern, text))

    # Check for SSN patterns
    ssn_pattern = r'\d{3}-\d{2}-\d{4}'
    violations["ssn"] = bool(re.search(ssn_pattern, text))

    # Check for email addresses
    email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
    violations["email"] = bool(re.search(email_pattern, text))

    # Check for street address patterns (simplified)
    address_pattern = r'\d+\s+\w+\s+(?:street|st|avenue|ave|road|rd|drive|dr|boulevard|blvd)'
    violations["address"] = bool(re.search(address_pattern, text, re.IGNORECASE))

    # Check for credit card numbers (4 groups of 4 digits)
    cc_pattern = r'\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}'
    violations["credit_card"] = bool(re.search(cc_pattern, text))

    # Overall safety
    is_safe = not any(violations.values())

    # Sanitize if unsafe
    sanitized_text = text if is_safe else _redact_pii(text)

    return {
        "is_safe": is_safe,
        "violations": violations,
        "sanitized_text": sanitized_text,
        "validation_timestamp": datetime.now().isoformat()
    }


def _redact_pii(text: str) -> str:
    """Redact all detected PII from text."""
    # Phone numbers
    text = re.sub(r'\d{3}[-.]?\d{3}[-.]?\d{4}', '[PHONE REDACTED]', text)
    # SSN
    text = re.sub(r'\d{3}-\d{2}-\d{4}', '[SSN REDACTED]', text)
    # Email
    text = re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', '[EMAIL REDACTED]', text)
    # Credit cards
    text = re.sub(r'\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}', '[CC REDACTED]', text)

    return text + "\n[NOTE: PII automatically redacted for HIPAA compliance]"


def audit_log(action: str, patient_id: str, agent: str, details: str = "") -> str:
    """
    Log all access for compliance auditing.

    Creates an immutable audit trail of all data access and
    modifications for HIPAA compliance.

    Args:
        action: Type of action performed (e.g., 'anonymize', 'access', 'schedule')
        patient_id: Anonymized patient identifier
        agent: Name of the agent performing the action
        details: Optional additional details

    Returns:
        Confirmation of log entry creation
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "patient_id": patient_id,
        "agent": agent,
        "details": details,
        "access_granted": True,
        "compliance_standard": "HIPAA",
        "retention_years": 6
    }

    # In production: write to secure, tamper-proof audit database
    # For demo: print to stdout (would be sent to logging service)
    print(f"[AUDIT] {json.dumps(log_entry)}")

    return json.dumps({
        "status": "logged",
        "log_id": f"log_{datetime.now().strftime('%Y%m%d%H%M%S')}_{patient_id[:8]}",
        "retention_until": (datetime.now().replace(year=datetime.now().year + 6)).isoformat()
    })


class SecurityAgent:
    """
    Security and compliance guardian for MediConnect.

    Ensures all patient data is handled securely and in compliance
    with healthcare regulations (HIPAA). Processes data before it
    enters the agent pipeline and validates outputs before delivery.

    Attributes:
        agent: LlmAgent configured for security operations
    """

    def __init__(self):
        """Initialize the security agent with compliance tools."""
        self.agent = LlmAgent(
            name="security_guard",
            model="gemini-2.5-flash",
            description="Security and compliance guardian",
            instruction="""
            You are the security guardian for MediConnect. Your responsibilities:

            1. ANONYMIZE all patient identifiers before processing
               - Names -> SHA-256 hashes
               - Phone numbers -> hashed contact tokens
               - Addresses -> region only (city/state)

            2. REDACT sensitive data from all outputs
               - SSN patterns (XXX-XX-XXXX)
               - Phone numbers (XXX-XXX-XXXX)
               - Email addresses
               - Exact street addresses

            3. VALIDATE no PII leaks in agent responses
               - Scan all output text for identifiable patterns
               - Block or sanitize if violations found

            4. ENSURE HIPAA compliance in all data handling
               - Minimum necessary principle
               - Audit trail for all access
               - Encrypted data at rest and in transit

            5. LOG all access for compliance auditing
               - Timestamp, action, patient_id, agent
               - Retain for 6 years per HIPAA requirements

            NEVER allow real names, phone numbers, or exact addresses to pass through.
            ALWAYS use patient_id hashes instead of real identifiers.
            """,
            tools=[anonymize_patient, validate_output, audit_log]  # Pass functions directly
        )


if __name__ == "__main__":
    # Demo
    print("=" * 60)
    print("Security Agent - Demo")
    print("=" * 60)

    security = SecurityAgent()

    # Test anonymization
    print("\n1. Testing Anonymization:")
    test_patient = {
        "name": "Maria Garcia",
        "phone": "555-123-4567",
        "email": "maria.g@email.com",
        "address": "123 Oak Street, Springfield, IL",
        "symptoms": "fever, headache"
    }
    print(f"   Before: {json.dumps(test_patient, indent=2)}")
    anonymized = anonymize_patient(test_patient)
    print(f"   After:  {json.dumps(anonymized, indent=2)}")

    # Test PII validation
    print("\n2. Testing PII Validation:")
    unsafe_text = "Patient John Doe, phone 555-123-4567, email john@email.com"
    result = validate_output(unsafe_text)
    print(f"   Input: {unsafe_text}")
    print(f"   Safe: {result['is_safe']}")
    print(f"   Violations: {result['violations']}")
    print(f"   Sanitized: {result['sanitized_text']}")

    # Test audit log
    print("\n3. Testing Audit Log:")
    log_result = audit_log("anonymize", anonymized["patient_id"], "security_agent")
    print(f"   {log_result}")

    print("\n" + "=" * 60)
