"""
Triage Agent Tools
==================
Additional tools for the triage agent.
Demonstrates: Agent skills (ADK tools)

NOTE: In Google ADK, tools are plain Python functions.
NO decorator needed - just pass them to LlmAgent(tools=[...])
"""
import json


def calculate_bmi(weight_kg: float, height_m: float) -> str:
    """
    Calculate Body Mass Index (BMI) for health assessment.

    Args:
        weight_kg: Weight in kilograms
        height_m: Height in meters

    Returns:
        BMI value and category
    """
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return json.dumps({
        "bmi": round(bmi, 1),
        "category": category,
        "recommendation": "Consult doctor if BMI < 18.5 or > 30"
    })


def assess_pediatric_urgency(age_months: int, symptoms: str) -> str:
    """
    Assess urgency for pediatric patients (special rules for children).

    Args:
        age_months: Age in months
        symptoms: Description of symptoms

    Returns:
        Urgency assessment with pediatric-specific guidance
    """
    # Infants < 3 months have lower threshold for urgent care
    if age_months < 3:
        if "fever" in symptoms.lower():
            return json.dumps({
                "urgency": "URGENT",
                "reason": "Any fever in infants < 3 months requires immediate evaluation",
                "action": "Go to ER or urgent care now"
            })

    # Children < 2 years
    if age_months < 24:
        if "dehydration" in symptoms.lower() or "not drinking" in symptoms.lower():
            return json.dumps({
                "urgency": "URGENT",
                "reason": "Dehydration risk in young children",
                "action": "Seek same-day care"
            })

    return json.dumps({
        "urgency": "ASSESS_FURTHER",
        "reason": "Standard pediatric assessment needed",
        "action": "Continue with full triage evaluation"
    })
