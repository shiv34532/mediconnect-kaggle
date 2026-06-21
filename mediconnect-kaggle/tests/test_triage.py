"""
Tests for Triage Agent
======================
Unit tests for symptom analysis and care recommendation.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.triage.agent import TriageAgent, search_medical_kb, check_drug_interactions
import json


def test_triage_agent_initialization():
    """Test that triage agent initializes correctly."""
    triage = TriageAgent()
    assert triage.agent is not None
    assert triage.agent.name == "triage_specialist"
    print("✓ Triage agent initialized")


def test_medical_kb_search():
    """Test medical knowledge base search."""
    # Test known symptoms (direct function call, no decorator)
    result = search_medical_kb("chest pain")
    assert "EMERGENCY" in result
    print("✓ Chest pain -> EMERGENCY")

    result = search_medical_kb("fever")
    assert "URGENT" in result or "NON-URGENT" in result
    print("✓ Fever -> appropriate level")

    # Test unknown symptom
    result = search_medical_kb("random unknown symptom xyz")
    assert "General" in result
    print("✓ Unknown symptom -> general guidance")


def test_drug_interactions():
    """Test drug interaction checking."""
    # Test dangerous combo (direct function call)
    result = check_drug_interactions("warfarin, aspirin")
    assert "WARNING" in result
    print("✓ Warfarin + Aspirin -> WARNING")

    # Test safe combo
    result = check_drug_interactions("vitamin D, calcium")
    assert "No known" in result
    print("✓ Vitamin D + Calcium -> Safe")


def test_triage_levels():
    """Test all triage levels are covered."""
    test_cases = [
        ("chest pain", "EMERGENCY"),
        ("difficulty breathing", "EMERGENCY"),
        ("fever", "URGENT"),
        ("headache", "SELF-CARE"),
    ]

    for symptom, expected_level in test_cases:
        result = search_medical_kb(symptom)
        assert expected_level in result, f"Expected {expected_level} for {symptom}"
        print(f"✓ {symptom} -> contains {expected_level}")


if __name__ == "__main__":
    print("=" * 60)
    print("Running Triage Agent Tests")
    print("=" * 60)

    test_triage_agent_initialization()
    test_medical_kb_search()
    test_drug_interactions()
    test_triage_levels()

    print("\n" + "=" * 60)
    print("All Triage Tests Passed! ✓")
    print("=" * 60)
