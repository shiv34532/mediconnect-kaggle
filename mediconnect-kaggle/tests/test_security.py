"""
Tests for Security Agent
=========================
Unit tests for HIPAA compliance, anonymization, and PII handling.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.security.agent import SecurityAgent, anonymize_patient, validate_output, audit_log
from shared.security import SecureDataHandler
import json


def test_security_agent_initialization():
    """Test security agent initializes."""
    security = SecurityAgent()
    assert security.agent is not None
    print("✓ Security agent initialized")


def test_anonymization():
    """Test patient data anonymization."""
    patient = {
        "name": "John Doe",
        "phone": "555-123-4567",
        "email": "john@email.com",
        "address": "123 Main St, Springfield, IL",
        "symptoms": "headache"
    }

    result = anonymize_patient(patient)

    # Verify PII is removed
    assert "name" not in result
    assert "phone" not in result
    assert "email" not in result
    assert "address" not in result

    # Verify hashes are present
    assert "patient_id" in result
    assert "contact_hash" in result
    assert "email_hash" in result
    assert "region" in result

    # Verify non-PII preserved
    assert result["symptoms"] == "headache"

    print("✓ PII anonymized correctly")
    print(f"   Patient ID: {result['patient_id']}")
    print(f"   Region: {result['region']}")


def test_pii_validation():
    """Test PII detection in output."""
    # Unsafe text with PII
    unsafe_text = "Patient John Doe, phone 555-123-4567, email john@email.com"
    result = validate_output(unsafe_text)

    assert result["is_safe"] == False
    assert result["violations"]["phone"] == True
    assert result["violations"]["email"] == True
    print("✓ PII detected in unsafe text")

    # Safe text
    safe_text = "Patient ID a3f5b7e2 reported fever and headache"
    result = validate_output(safe_text)
    assert result["is_safe"] == True
    print("✓ Safe text passed validation")


def test_audit_logging():
    """Test audit log creation."""
    result = json.loads(audit_log("test_action", "anon_12345", "test_agent"))
    assert result["status"] == "logged"
    assert "log_id" in result
    print(f"✓ Audit log created: {result['log_id']}")


def test_encryption():
    """Test data encryption/decryption."""
    handler = SecureDataHandler()

    sensitive = "Patient has diabetes and hypertension"
    encrypted = handler.encrypt(sensitive)
    decrypted = handler.decrypt(encrypted)

    assert decrypted == sensitive
    assert encrypted != sensitive
    print("✓ Encryption/decryption works correctly")


def test_hashing():
    """Test identifier hashing."""
    handler = SecureDataHandler()

    hash1 = handler.hash_identifier("Maria Garcia")
    hash2 = handler.hash_identifier("Maria Garcia")
    hash3 = handler.hash_identifier("John Smith")

    assert hash1 == hash2  # Same input -> same hash
    assert hash1 != hash3  # Different input -> different hash
    assert len(hash1) == 16
    print("✓ Hashing is deterministic and unique")


if __name__ == "__main__":
    print("=" * 60)
    print("Running Security Agent Tests")
    print("=" * 60)

    test_security_agent_initialization()
    test_anonymization()
    test_pii_validation()
    test_audit_logging()
    test_encryption()
    test_hashing()

    print("\n" + "=" * 60)
    print("All Security Tests Passed! ✓")
    print("=" * 60)
