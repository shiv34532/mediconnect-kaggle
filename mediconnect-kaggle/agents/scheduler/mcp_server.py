"""
MCP Server for Healthcare Appointment Scheduling
=================================================
Demonstrates: MCP Server concept

A Model Context Protocol (MCP) server that exposes clinic scheduling
tools to AI agents. Uses FastMCP for simple, fast implementation.

Tools:
- list_available_slots: Query available appointment times
- book_appointment: Book a slot for a patient
- cancel_appointment: Cancel a booked appointment
"""
from mcp.server.fastmcp import FastMCP
from datetime import datetime, timedelta
import json

# Initialize MCP server with name
mcp = FastMCP("healthcare_scheduler")

# Mock clinic database
# In production, this connects to a real clinic management system
CLINIC_DB = {
    "rural_clinic_001": {
        "name": "Sunrise Community Health Center",
        "address": "123 Main St, Rural County",
        "phone": "555-0100",
        "doctors": ["Dr. Sarah Smith", "Dr. Maria Garcia", "Dr. James Johnson"],
        "specialties": ["Family Medicine", "Pediatrics", "Women's Health"],
        "hours": {
            "weekday": "9:00 AM - 5:00 PM",
            "saturday": "9:00 AM - 1:00 PM",
            "sunday": "Closed"
        }
    },
    "rural_clinic_002": {
        "name": "Valley Health Clinic",
        "address": "456 Oak Ave, Valley Township",
        "phone": "555-0200",
        "doctors": ["Dr. Emily Chen", "Dr. Robert Brown"],
        "specialties": ["Internal Medicine", "Geriatrics"],
        "hours": {
            "weekday": "8:00 AM - 6:00 PM",
            "saturday": "9:00 AM - 12:00 PM",
            "sunday": "Closed"
        }
    },
    "urban_clinic_001": {
        "name": "City Central Medical",
        "address": "789 Downtown Blvd, Metro City",
        "phone": "555-0300",
        "doctors": ["Dr. Michael Lee", "Dr. Aisha Patel", "Dr. David Wilson", "Dr. Lisa Anderson"],
        "specialties": ["Family Medicine", "Cardiology", "Dermatology", "Mental Health"],
        "hours": {
            "weekday": "7:00 AM - 8:00 PM",
            "saturday": "8:00 AM - 4:00 PM",
            "sunday": "10:00 AM - 2:00 PM"
        }
    }
}

# Generate mock appointment slots
def generate_slots(clinic_id: str, days_ahead: int = 7) -> list:
    """Generate available appointment slots for a clinic."""
    slots = []
    base = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)

    clinic = CLINIC_DB.get(clinic_id, {})
    doctors = clinic.get("doctors", ["Dr. General"])

    for day in range(days_ahead):
        date = base + timedelta(days=day)

        # Skip Sunday for most clinics
        if date.weekday() == 6 and clinic_id != "urban_clinic_001":
            continue

        # Weekend hours
        if date.weekday() >= 5:  # Saturday or Sunday
            start_hour = 9
            end_hour = 13 if date.weekday() == 5 else 14  # Sat 1pm, Sun 2pm for urban
        else:
            start_hour = 9
            end_hour = 17

        for hour in range(start_hour, end_hour):
            for minute in [0, 30]:  # 30-minute slots
                doctor = doctors[(hour + day) % len(doctors)]
                slot_time = date.replace(hour=hour, minute=minute)
                slots.append({
                    "datetime": slot_time.isoformat(),
                    "doctor": doctor,
                    "available": True,
                    "duration_minutes": 30,
                    "type": "in-person",
                    "room": f"Room {((hour + minute) % 10) + 1}"
                })

    return slots

# Initialize slots for all clinics
APPOINTMENT_DB = {}
for clinic_id in CLINIC_DB:
    APPOINTMENT_DB[clinic_id] = generate_slots(clinic_id)


@mcp.tool()
def list_available_slots(clinic_id: str, date: str = None, specialty: str = None) -> str:
    """
    List available appointment slots for a clinic.

    Query the clinic scheduling system for open appointment slots
    that match the specified criteria.

    Args:
        clinic_id: Unique clinic identifier (e.g., 'rural_clinic_001')
        date: Optional date filter (YYYY-MM-DD format)
        specialty: Optional specialty filter (e.g., 'Pediatrics')

    Returns:
        JSON string with clinic info and available slots

    Example:
        >>> list_available_slots("rural_clinic_001", "2026-06-21")
        '{"clinic": "Sunrise Community Health", "slots": [...]}'
    """
    clinic = CLINIC_DB.get(clinic_id)
    if not clinic:
        return json.dumps({
            "error": "Clinic not found",
            "available_clinics": list(CLINIC_DB.keys())
        })

    slots = APPOINTMENT_DB.get(clinic_id, [])

    # Filter by date if specified
    if date:
        slots = [s for s in slots if s["datetime"].startswith(date)]

    # Filter by specialty if specified
    if specialty:
        # Simplified: all doctors can handle all specialties in demo
        pass

    # Only return available slots
    available = [s for s in slots if s["available"]]

    return json.dumps({
        "clinic": clinic["name"],
        "clinic_id": clinic_id,
        "address": clinic["address"],
        "phone": clinic["phone"],
        "specialties": clinic["specialties"],
        "hours": clinic["hours"],
        "total_available": len(available),
        "available_slots": available[:10]  # Return top 10
    }, indent=2)


@mcp.tool()
def book_appointment(clinic_id: str, slot_time: str, patient_id: str, 
                     reason: str = "General consultation") -> str:
    """
    Book an appointment slot.

    Reserve an appointment slot for a patient at the specified clinic.

    Args:
        clinic_id: Clinic identifier
        slot_time: ISO datetime string (e.g., '2026-06-21T10:00:00')
        patient_id: Anonymized patient identifier
        reason: Visit reason (default: General consultation)

    Returns:
        JSON string with booking confirmation details

    Example:
        >>> book_appointment("rural_clinic_001", "2026-06-21T10:00:00", "anon_12345")
        '{"status": "confirmed", "appointment_id": "appt_..."}'
    """
    clinic = CLINIC_DB.get(clinic_id)
    if not clinic:
        return json.dumps({
            "error": "Clinic not found",
            "available_clinics": list(CLINIC_DB.keys())
        })

    slots = APPOINTMENT_DB.get(clinic_id, [])

    # Find and book the slot
    for slot in slots:
        if slot["datetime"] == slot_time and slot["available"]:
            slot["available"] = False
            slot["patient_id"] = patient_id
            slot["reason"] = reason
            slot["booked_at"] = datetime.now().isoformat()

            appointment_id = f"appt_{patient_id}_{slot_time.replace(':', '').replace('-', '')}"

            return json.dumps({
                "status": "confirmed",
                "appointment_id": appointment_id,
                "clinic": clinic["name"],
                "clinic_id": clinic_id,
                "doctor": slot["doctor"],
                "time": slot_time,
                "duration": f"{slot['duration_minutes']} minutes",
                "room": slot["room"],
                "reason": reason,
                "confirmation_code": appointment_id[-8:].upper(),
                "instructions": [
                    "Arrive 15 minutes early",
                    "Bring photo ID and insurance card",
                    "Complete pre-visit questionnaire online",
                    f"Call {clinic['phone']} if you need to reschedule"
                ]
            }, indent=2)

    return json.dumps({
        "error": "Slot not available",
        "message": "The requested time slot is no longer available. Please check for other slots.",
        "suggestion": "Use list_available_slots to find alternative times"
    })


@mcp.tool()
def cancel_appointment(appointment_id: str) -> str:
    """
    Cancel a booked appointment.

    Cancel an existing appointment and free up the slot.

    Args:
        appointment_id: Appointment identifier to cancel

    Returns:
        JSON string with cancellation confirmation

    Example:
        >>> cancel_appointment("appt_anon_12345_202606211000")
        '{"status": "cancelled", "refund": "No charge"}'
    """
    # Find and cancel the appointment
    for clinic_id, slots in APPOINTMENT_DB.items():
        for slot in slots:
            if not slot["available"]:
                # Reconstruct appointment ID to match
                patient_id = slot.get("patient_id", "")
                slot_time = slot["datetime"].replace(":", "").replace("-", "")
                check_id = f"appt_{patient_id}_{slot_time}"

                if check_id == appointment_id:
                    slot["available"] = True
                    slot.pop("patient_id", None)
                    slot.pop("reason", None)
                    slot.pop("booked_at", None)

                    return json.dumps({
                        "status": "cancelled",
                        "appointment_id": appointment_id,
                        "clinic": CLINIC_DB[clinic_id]["name"],
                        "message": "Appointment cancelled successfully",
                        "refund_policy": "No charge for cancellations 24+ hours in advance",
                        "reschedule": "Use list_available_slots to book a new appointment"
                    }, indent=2)

    return json.dumps({
        "error": "Appointment not found",
        "message": "Could not locate the specified appointment ID"
    })


@mcp.tool()
def get_clinic_info(clinic_id: str) -> str:
    """
    Get information about a clinic.

    Args:
        clinic_id: Clinic identifier

    Returns:
        JSON string with clinic details
    """
    clinic = CLINIC_DB.get(clinic_id)
    if not clinic:
        return json.dumps({
            "error": "Clinic not found",
            "available_clinics": list(CLINIC_DB.keys())
        })

    return json.dumps({
        "clinic_id": clinic_id,
        **clinic
    }, indent=2)


@mcp.tool()
def list_all_clinics() -> str:
    """
    List all available clinics in the system.

    Returns:
        JSON string with all clinic summaries
    """
    clinics = []
    for clinic_id, info in CLINIC_DB.items():
        clinics.append({
            "clinic_id": clinic_id,
            "name": info["name"],
            "address": info["address"],
            "specialties": info["specialties"],
            "phone": info["phone"]
        })

    return json.dumps({
        "total_clinics": len(clinics),
        "clinics": clinics
    }, indent=2)


if __name__ == "__main__":
    # Run the MCP server
    print("=" * 60)
    print("Healthcare MCP Server")
    print("=" * 60)
    print("\nStarting MCP server on stdio transport...")
    print("Tools available:")
    print("  - list_available_slots")
    print("  - book_appointment")
    print("  - cancel_appointment")
    print("  - get_clinic_info")
    print("  - list_all_clinics")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)

    mcp.run(transport="stdio")
