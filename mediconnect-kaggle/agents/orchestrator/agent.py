"""
MediConnect Orchestrator Agent
================================
Coordinates the multi-agent healthcare system.
Demonstrates: Agent / Multi-agent system (ADK)

This is the central coordinator that routes patient requests through:
1. Security Agent (anonymization, HIPAA compliance)
2. Translator Agent (language processing)
3. Triage Agent (symptom analysis)
4. Scheduler Agent (appointment booking via MCP)
"""
import os
import sys
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent, SequentialAgent

# Import sub-agents
from agents.triage.agent import TriageAgent
from agents.translator.agent import TranslatorAgent
from agents.scheduler.agent import SchedulerAgent
from agents.security.agent import SecurityAgent


class MediConnectOrchestrator:
    """
    Main orchestrator for the MediConnect healthcare access system.

    Manages a SequentialAgent pipeline that processes patient requests
    through security, translation, triage, and scheduling stages.

    Attributes:
        security_agent: Handles anonymization and HIPAA compliance
        translator_agent: Processes multilingual patient input
        triage_agent: Performs symptom analysis and care recommendations
        scheduler_agent: Books appointments via MCP server
        workflow: SequentialAgent pipeline coordinating all sub-agents
    """

    def __init__(self):
        """Initialize all sub-agents and build the sequential pipeline."""
        print("[Orchestrator] Initializing MediConnect system...")

        # Initialize sub-agents
        self.security_agent = SecurityAgent()
        print("[Orchestrator] ✓ Security agent loaded")

        self.translator_agent = TranslatorAgent()
        print("[Orchestrator] ✓ Translator agent loaded")

        self.triage_agent = TriageAgent()
        print("[Orchestrator] ✓ Triage agent loaded")

        self.scheduler_agent = SchedulerAgent()
        print("[Orchestrator] ✓ Scheduler agent loaded")

        # Build the sequential pipeline
        # Each agent's output becomes the next agent's input
        self.workflow = SequentialAgent(
            name="mediconnect_pipeline",
            description="Healthcare access pipeline for underserved communities",
            sub_agents=[
                self.security_agent.agent,      # Step 1: Security validation
                self.translator_agent.agent,    # Step 2: Language processing
                self.triage_agent.agent,        # Step 3: Medical triage
                self.scheduler_agent.agent      # Step 4: Appointment booking
            ]
        )
        print("[Orchestrator] ✓ Sequential pipeline built")
        print("[Orchestrator] Ready for patient requests!")

    def process_patient_request(self, patient_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for processing patient healthcare requests.

        Args:
            patient_input: Dictionary containing:
                - patient_id: Anonymized patient identifier
                - language: Patient's preferred language code (e.g., 'es', 'fr')
                - symptoms: Description of symptoms (in patient's language)
                - location: Clinic identifier for scheduling
                - urgency: Optional urgency hint from patient

        Returns:
            Dictionary with:
                - status: 'success' or 'error'
                - triage_level: EMERGENCY, URGENT, NON-URGENT, or SELF-CARE
                - recommended_action: Specific next steps
                - appointment: Booking details if scheduled
                - security_log: Audit trail entry

        Example:
            >>> orchestrator = MediConnectOrchestrator()
            >>> result = orchestrator.process_patient_request({
            ...     "patient_id": "anon_12345",
            ...     "language": "es",
            ...     "symptoms": "fiebre, dolor de cabeza",
            ...     "location": "rural_clinic_001"
            ... })
        """
        print(f"\n[Orchestrator] Received patient request: {patient_input.get('patient_id', 'unknown')}")

        try:
            # The orchestrator delegates to the sequential pipeline
            # Each agent processes and enriches the data
            result = self.workflow.run(input=patient_input)

            # Add metadata to result
            result["status"] = "success"
            result["pipeline_version"] = "1.0.0"
            result["track"] = "Agents for Good"

            print(f"[Orchestrator] ✓ Request processed successfully")
            return result

        except Exception as e:
            print(f"[Orchestrator] ✗ Error processing request: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "message": "Please try again or contact emergency services if urgent"
            }

    def get_system_status(self) -> str:
        """
        Check the health status of all agents in the system.

        Returns:
            JSON string with status of each agent component.
        """
        import json
        status = {
            "orchestrator": "healthy",
            "security_agent": "loaded" if self.security_agent else "error",
            "translator_agent": "loaded" if self.translator_agent else "error",
            "triage_agent": "loaded" if self.triage_agent else "error",
            "scheduler_agent": "loaded" if self.scheduler_agent else "error",
            "pipeline": "active" if self.workflow else "error"
        }
        return json.dumps(status, indent=2)


# Standalone agent definition for ADK CLI usage
# This allows running: adk run agents/orchestrator
orchestrator_agent = LlmAgent(
    name="mediconnect_orchestrator",
    model="gemini-2.5-flash",
    description="Orchestrates healthcare access for underserved communities",
    instruction="""
    You are the MediConnect Orchestrator. Your job is to coordinate healthcare 
    access for patients in underserved communities.

    WORKFLOW:
    1. SECURITY: Validate patient data for HIPAA compliance, anonymize PII
    2. TRANSLATION: If patient speaks non-English, translate symptoms accurately
    3. TRIAGE: Analyze symptoms and recommend care level (EMERGENCY/URGENT/NON-URGENT/SELF-CARE)
    4. SCHEDULING: Book appropriate appointment if needed via MCP server

    SAFETY RULES:
    - Always prioritize patient safety
    - For emergency symptoms (chest pain, difficulty breathing, severe bleeding), 
      immediately escalate to emergency services
    - Never provide definitive diagnosis, only triage recommendations
    - Include disclaimer that this is not a substitute for professional medical advice

    OUTPUT FORMAT:
    Provide clear, actionable guidance in the patient's preferred language.
    """,
    tools=[]  # Sub-agents handle the tools internally
)


if __name__ == "__main__":
    # Demo run
    print("=" * 60)
    print("MediConnect Orchestrator - Demo Run")
    print("=" * 60)

    orchestrator = MediConnectOrchestrator()

    # Demo: Spanish-speaking patient in rural clinic
    demo_request = {
        "patient_id": "anon_demo_001",
        "language": "es",
        "symptoms": "fiebre, dolor de cabeza, tos desde hace 2 días",
        "location": "rural_clinic_001",
        "urgency": "non-urgent"
    }

    print("\nDemo Patient Request:")
    print(f"  Language: Spanish")
    print(f"  Symptoms: {demo_request['symptoms']}")
    print(f"  Location: {demo_request['location']}")

    result = orchestrator.process_patient_request(demo_request)

    print("\nResult:")
    print(f"  {result}")
    print("\n" + "=" * 60)
