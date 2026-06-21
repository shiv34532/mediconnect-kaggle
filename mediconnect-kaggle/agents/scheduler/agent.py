"""
Appointment Scheduler Agent
===========================
Handles appointment scheduling via MCP server integration.
Demonstrates: MCP Server integration

Connects to a Model Context Protocol (MCP) server to interact with
clinic scheduling systems for listing, booking, and canceling appointments.

NOTE: In Google ADK, tools are plain Python functions.
NO decorator needed - just pass them to LlmAgent(tools=[...])
"""
from google.adk.agents import LlmAgent
import json
from datetime import datetime, timedelta


# Tool functions - plain Python functions, NO decorator needed
def list_slots(clinic_id: str, date: str = None) -> str:
    """
    List available appointment slots for a clinic.

    Wraps the MCP server tool to query available appointment times.
    In production, this connects to the actual MCP server.

    Args:
        clinic_id: Unique clinic identifier (e.g., 'rural_clinic_001')
        date: Optional date filter (YYYY-MM-DD format)

    Returns:
        JSON string with available slots

    Example:
        >>> list_slots("rural_clinic_001", "2026-06-21")
        '{"clinic_id": "rural_clinic_001", "slots": [...]}'
    """
    # In production, this would call the MCP server
    # For demo, generate mock slots
    slots = _generate_mock_slots(clinic_id, date)

    return json.dumps({
        "clinic_id": clinic_id,
        "date": date or "next_available",
        "available_slots": slots,
        "total_available": len(slots)
    })


def book_slot(clinic_id: str, slot_time: str, patient_id: str, 
              reason: str = "General consultation") -> str:
    """
    Book an appointment slot.

    Wraps the MCP server tool to book appointments.

    Args:
        clinic_id: Clinic identifier
        slot_time: ISO datetime string (e.g., '2026-06-21T10:00:00')
        patient_id: Anonymized patient identifier
        reason: Visit reason (default: General consultation)

    Returns:
        JSON string with booking confirmation
    """
    # Generate appointment ID
    appt_id = f"appt_{patient_id}_{slot_time.replace(':', '').replace('-', '')}"

    return json.dumps({
        "status": "confirmed",
        "appointment_id": appt_id,
        "clinic_id": clinic_id,
        "patient_id": patient_id,
        "scheduled_time": slot_time,
        "reason": reason,
        "confirmation_code": appt_id[-8:].upper(),
        "instructions": "Arrive 15 minutes early. Bring ID and insurance card."
    })


def cancel_slot(appointment_id: str) -> str:
    """
    Cancel a booked appointment.

    Args:
        appointment_id: Appointment identifier to cancel

    Returns:
        JSON string with cancellation confirmation
    """
    return json.dumps({
        "status": "cancelled",
        "appointment_id": appointment_id,
        "message": "Appointment cancelled successfully. You may reschedule using the booking tool.",
        "refund_policy": "No charge for cancellations 24+ hours in advance"
    })


def _generate_mock_slots(clinic_id: str, date: str = None) -> list:
    """Generate mock appointment slots for demonstration."""
    slots = []
    base = datetime.now()

    # Generate slots for next 3 days
    for day_offset in range(3):
        date_obj = base + timedelta(days=day_offset)
        if date and date_obj.strftime("%Y-%m-%d") != date:
            continue

        for hour in range(9, 17):  # 9 AM to 5 PM
            for minute in [0, 30]:  # 30-minute slots
                slot_time = date_obj.replace(hour=hour, minute=minute)
                slots.append({
                    "datetime": slot_time.isoformat(),
                    "doctor": "Dr. Smith" if hour % 2 == 0 else "Dr. Garcia",
                    "duration_minutes": 30,
                    "type": "in-person"
                })

    return slots[:5]  # Return top 5 slots


class SchedulerAgent:
    """
    Agent that handles appointment scheduling via MCP server.

    Wraps MCP tools for use within the ADK agent framework, allowing
    the LLM to reason about and execute scheduling operations.

    Attributes:
        agent: LlmAgent configured for appointment scheduling
    """

    def __init__(self):
        """Initialize the scheduler agent with MCP tools."""
        self.agent = LlmAgent(
            name="scheduler",
            model="gemini-2.5-flash",
            description="Healthcare appointment scheduler",
            instruction="""
            You are an appointment scheduling assistant. Help patients book 
            appropriate appointments based on triage recommendations.

            SCHEDULING RULES:
            - EMERGENCY patients: Do NOT schedule - direct to ER immediately
            - URGENT patients: Schedule same-day or next-day slots
            - NON-URGENT patients: Schedule within 1-3 business days
            - SELF-CARE patients: No appointment needed, provide home care instructions

            CLINIC HOURS:
            - Weekdays: 9:00 AM - 5:00 PM
            - Saturday: 9:00 AM - 1:00 PM
            - Sunday: Closed

            BOOKING PROCESS:
            1. Confirm patient details and preferred time
            2. Check availability using list_slots tool
            3. Book appointment using book_slot tool
            4. Provide confirmation with appointment ID

            Always confirm details with the patient before booking.
            Provide clear instructions for appointment preparation.
            """,
            tools=[list_slots, book_slot, cancel_slot]  # Pass functions directly
        )


if __name__ == "__main__":
    # Demo
    print("=" * 60)
    print("Scheduler Agent - Demo")
    print("=" * 60)

    scheduler = SchedulerAgent()

    print("\n1. Listing available slots:")
    slots = json.loads(list_slots("rural_clinic_001"))
    print(f"   Found {slots['total_available']} slots")
    print(f"   First slot: {slots['available_slots'][0]}")

    print("\n2. Booking appointment:")
    booking = json.loads(book_slot(
        "rural_clinic_001",
        "2026-06-21T10:00:00",
        "anon_12345",
        "Fever and headache follow-up"
    ))
    print(f"   Status: {booking['status']}")
    print(f"   Appointment ID: {booking['appointment_id']}")
    print(f"   Confirmation: {booking['confirmation_code']}")

    print("\n" + "=" * 60)
