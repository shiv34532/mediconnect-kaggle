"""
Medical Triage Agent
====================
Performs symptom analysis and care level recommendation.
Demonstrates: Agent / Multi-agent system (ADK)

Uses evidence-based protocols to recommend care levels:
- EMERGENCY: Life-threatening, immediate intervention needed
- URGENT: Needs same-day care
- NON-URGENT: Can wait for scheduled primary care
- SELF-CARE: Minor issue, home treatment sufficient
"""
from google.adk.agents import LlmAgent
import json


# Tool functions - plain Python functions, NO decorator needed
def search_medical_kb(query: str) -> str:
    """
    Search medical knowledge base for symptom information.

    Provides evidence-based guidance for common symptoms to support
    triage decisions. In production, this connects to a comprehensive
    medical knowledge base or RAG system.

    Args:
        query: Symptom or medical term to search for

    Returns:
        String with medical guidance for the queried symptom

    Example:
        >>> search_medical_kb("chest pain")
        'Potential cardiac issue - escalate to EMERGENCY'
    """
    # Simplified medical knowledge base for demonstration
    # In production, this would connect to a real medical database or RAG
    knowledge_base = {
        "chest pain": (
            "Potential cardiac issue - escalate to EMERGENCY. "
            "Possible causes: myocardial infarction, angina, pulmonary embolism. "
            "Action: Call emergency services immediately."
        ),
        "difficulty breathing": (
            "Respiratory distress - escalate to EMERGENCY. "
            "Possible causes: asthma attack, allergic reaction, pneumonia, heart failure. "
            "Action: Call emergency services immediately."
        ),
        "severe bleeding": (
            "Hemorrhage - escalate to EMERGENCY. "
            "Apply direct pressure while waiting for emergency services."
        ),
        "fever": (
            "Check duration and severity. "
            ">3 days or >103°F (39.4°C) = URGENT. "
            "<3 days and <103°F = NON-URGENT with monitoring. "
            "Watch for: stiff neck, confusion, rash (could indicate meningitis)."
        ),
        "headache": (
            "Assess severity and associated symptoms. "
            "'Worst headache of life' or with neurological symptoms = EMERGENCY. "
            "Mild, no other symptoms = SELF-CARE (rest, hydration, OTC pain relievers). "
            "Persistent >48hrs = NON-URGENT."
        ),
        "cough": (
            "Assess duration and characteristics. "
            "With blood or severe shortness of breath = URGENT. "
            "Dry cough <2 weeks = SELF-CARE. "
            "Productive cough >2 weeks = NON-URGENT (possible infection)."
        ),
        "rash": (
            "Check for associated symptoms. "
            "With breathing difficulty or swelling = EMERGENCY (anaphylaxis). "
            "With fever = URGENT. "
            "Localized, no other symptoms = SELF-CARE."
        ),
        "abdominal pain": (
            "Assess location and severity. "
            "Severe, localized, or with fever/vomiting = URGENT. "
            "Mild, diffuse, no other symptoms = SELF-CARE. "
            "Possible appendicitis if right lower quadrant = URGENT."
        ),
        "diabetes": (
            "Monitor blood sugar. "
            "Very high (>400) or very low (<50) with symptoms = EMERGENCY. "
            "Elevated but stable = NON-URGENT (adjust medication with doctor)."
        ),
        "pregnancy": (
            "Any bleeding, severe abdominal pain, or decreased fetal movement = EMERGENCY. "
            "Mild symptoms = consult OB/GYN (NON-URGENT to URGENT depending on severity)."
        )
    }

    # Search for best match
    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value

    return (
        "General symptom guidance: Assess severity, duration, and associated symptoms. "
        "When in doubt, escalate to higher care level. "
        "For persistent or worsening symptoms, seek medical evaluation."
    )


def check_drug_interactions(medications: str) -> str:
    """
    Check for dangerous drug interactions.

    Security feature that prevents harmful medical advice by checking
    for known dangerous drug combinations before recommendations.

    Args:
        medications: Comma-separated list of medication names

    Returns:
        Warning message if dangerous interaction found, otherwise safe status

    Example:
        >>> check_drug_interactions("warfarin, aspirin")
        'WARNING: Dangerous interaction detected: warfarin + aspirin (increased bleeding risk)'
    """
    # Known dangerous drug combinations
    # In production, use FDA API or clinical drug database
    dangerous_combos = [
        ("warfarin", "aspirin", "increased bleeding risk"),
        ("maoi", "ssri", "serotonin syndrome risk"),
        ("simvastatin", "clarithromycin", "muscle toxicity risk"),
        ("metformin", "contrast dye", "lactic acidosis risk"),
        ("lisinopril", "spironolactone", "hyperkalemia risk"),
    ]

    meds = [m.strip().lower() for m in medications.split(",")]

    warnings = []
    for drug1, drug2, risk in dangerous_combos:
        if drug1 in meds and drug2 in meds:
            warnings.append(f"WARNING: Dangerous interaction: {drug1} + {drug2} ({risk})")

    if warnings:
        return "\n".join(warnings) + "\n\nCONSULT DOCTOR BEFORE TAKING THESE TOGETHER."

    return "No known dangerous interactions detected. Always consult your pharmacist or doctor."


class TriageAgent:
    """
    Specialized agent for medical symptom triage.

    Analyzes patient symptoms and recommends appropriate care levels
    using evidence-based medical protocols. Integrates with a medical
    knowledge base and drug interaction checker.

    Attributes:
        agent: LlmAgent configured for medical triage tasks
    """

    def __init__(self):
        """Initialize the triage agent with medical tools."""
        self.agent = LlmAgent(
            name="triage_specialist",
            model="gemini-2.5-flash",
            description="Medical triage specialist for symptom assessment",
            instruction="""
            You are a medical triage specialist. Analyze patient symptoms and 
            recommend appropriate care levels.

            CARE LEVELS:
            - EMERGENCY: Life-threatening symptoms (chest pain, severe bleeding, 
              difficulty breathing, loss of consciousness). Patient should call 
              emergency services (911) immediately.
            - URGENT: Needs same-day care (high fever >103F, persistent vomiting, 
              severe pain, signs of infection). Recommend urgent care or ER.
            - NON-URGENT: Can wait for primary care appointment (mild fever, 
              cough, minor injuries). Schedule within 1-3 days.
            - SELF-CARE: Minor issues (mild headache, small cuts, common cold). 
              Recommend home treatment and monitoring.

            SAFETY RULES:
            - Always err on the side of caution - when in doubt, escalate
            - Ask clarifying questions if symptoms are vague or incomplete
            - Never provide definitive diagnosis, only triage level recommendation
            - Include disclaimer that this is not a substitute for professional medical advice
            - Consider patient age, pregnancy status, and chronic conditions

            OUTPUT FORMAT (JSON):
            {
                "triage_level": "EMERGENCY|URGENT|NON-URGENT|SELF-CARE",
                "reasoning": "Detailed explanation of why this level was chosen",
                "recommended_action": "Specific next step for patient",
                "warning_signs": ["Symptoms that would require immediate escalation"],
                "questions_to_ask": ["Optional follow-up questions for better assessment"]
            }
            """,
            tools=[search_medical_kb, check_drug_interactions]  # Pass functions directly
        )


if __name__ == "__main__":
    # Demo
    print("=" * 60)
    print("Triage Agent - Demo")
    print("=" * 60)

    triage = TriageAgent()

    # Test knowledge base
    print("\n1. Testing Medical Knowledge Base:")
    print(f"   Chest pain: {search_medical_kb('chest pain')[:80]}...")
    print(f"   Fever: {search_medical_kb('fever')[:80]}...")

    # Test drug interactions
    print("\n2. Testing Drug Interactions:")
    print(f"   Warfarin + Aspirin: {check_drug_interactions('warfarin, aspirin')}")
    print(f"   Safe combo: {check_drug_interactions('vitamin D, calcium')}")

    print("\n" + "=" * 60)
