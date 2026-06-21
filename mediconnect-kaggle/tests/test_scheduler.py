"""
Tests for Scheduler Agent & MCP Server
========================================
Unit tests for appointment scheduling and MCP tools.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.scheduler.agent import SchedulerAgent, list_slots, book_slot, cancel_slot
from agents.scheduler.mcp_server import list_available_slots, book_appointment, cancel_appointment
import json


def test_scheduler_initialization():
    """Test scheduler agent initializes."""
    scheduler = SchedulerAgent()
    assert scheduler.agent is not None
    print("✓ Scheduler agent initialized")


def test_list_slots():
    """Test listing available slots."""
    result = json.loads(list_slots("rural_clinic_001"))

    assert "available_slots" in result
    assert result["total_available"] > 0
    print(f"✓ Found {result['total_available']} available slots")


def test_mcp_list_slots():
    """Test MCP server list_available_slots tool."""
    result = json.loads(list_available_slots("rural_clinic_001"))
    assert "clinic" in result
    assert result["total_available"] > 0
    print(f"✓ MCP: Found {result['total_available']} slots at {result['clinic']}")


def test_mcp_book_appointment():
    """Test MCP server book_appointment tool."""
    # First get available slots
    slots_result = json.loads(list_available_slots("rural_clinic_001"))
    first_slot = slots_result["available_slots"][0]["datetime"]

    # Book it
    result = json.loads(book_appointment(
        "rural_clinic_001",
        first_slot,
        "anon_test_001",
        "Annual checkup"
    ))

    assert result["status"] == "confirmed"
    assert "appointment_id" in result
    print(f"✓ MCP: Booked appointment {result['appointment_id']}")

    return result["appointment_id"]


def test_mcp_cancel_appointment():
    """Test MCP server cancel_appointment tool."""
    appt_id = test_mcp_book_appointment()

    result = json.loads(cancel_appointment(appt_id))
    assert result["status"] == "cancelled"
    print(f"✓ MCP: Cancelled appointment {appt_id}")


def test_invalid_clinic():
    """Test handling of invalid clinic ID."""
    result = json.loads(list_available_slots("invalid_clinic"))
    assert "error" in result
    print("✓ Invalid clinic handled correctly")


if __name__ == "__main__":
    print("=" * 60)
    print("Running Scheduler Agent Tests")
    print("=" * 60)

    test_scheduler_initialization()
    test_list_slots()
    test_mcp_list_slots()
    test_mcp_book_appointment()
    test_mcp_cancel_appointment()
    test_invalid_clinic()

    print("\n" + "=" * 60)
    print("All Scheduler Tests Passed! ✓")
    print("=" * 60)
