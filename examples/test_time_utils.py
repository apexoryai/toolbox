#!/usr/bin/env python3
"""
Test script for time utility functions.
Demonstrates timezone-aware operations for the hotel management system.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.utils.time_utils import (
    get_current_time,
    validate_booking_dates,
    convert_time_between_timezones,
    get_business_hours,
    format_duration,
    resolve_timezone
)


def test_time_utilities():
    """Test all time utility functions."""
    print("🕐 Testing Time Utility Functions\n")
    
    # Test 1: Get current time
    print("1. Current Time (Mountain Time):")
    current_time = get_current_time("America/Denver")
    print(f"   {current_time}")
    print()
    
    # Test 2: Validate booking dates
    print("2. Booking Date Validation:")
    validation = validate_booking_dates("2025-07-15", "2025-07-18")
    print(f"   Valid booking: {validation}")
    print()
    
    # Test 3: Invalid booking dates
    print("3. Invalid Booking Dates:")
    invalid_validation = validate_booking_dates("2025-01-01", "2024-12-31")
    print(f"   Invalid booking: {invalid_validation}")
    print()
    
    # Test 4: Time conversion
    print("4. Time Zone Conversion:")
    conversion = convert_time_between_timezones("14:30", "America/Denver", "America/New_York")
    print(f"   2:30 PM MDT to EST: {conversion}")
    print()
    
    # Test 5: Business hours
    print("5. Business Hours:")
    business = get_business_hours("America/Denver")
    print(f"   Hotel business hours: {business}")
    print()
    
    # Test 6: Duration formatting
    print("6. Duration Formatting:")
    duration = format_duration("2025-07-15", "2025-07-18")
    print(f"   3-day booking: {duration}")
    
    long_duration = format_duration("2025-07-01", "2025-08-01")
    print(f"   31-day booking: {long_duration}")
    print()
    
    # Test 7: Timezone resolution
    print("7. Timezone Resolution:")
    friendly_tz = resolve_timezone("Mountain Time")
    print(f"   'Mountain Time' resolves to: {friendly_tz}")
    
    iana_tz = resolve_timezone("America/Denver")
    print(f"   'America/Denver' resolves to: {iana_tz}")
    print()
    
    # Test 8: Multiple timezones
    print("8. Multiple Timezones:")
    timezones = ["America/Denver", "America/New_York", "Europe/London", "Asia/Tokyo"]
    for tz in timezones:
        time_info = get_current_time(tz)
        print(f"   {tz}: {time_info.get('time', 'Error')}")
    print()


def test_booking_scenarios():
    """Test realistic booking scenarios."""
    print("🏨 Testing Booking Scenarios\n")
    
    scenarios = [
        {
            "name": "Valid future booking",
            "checkin": "2025-07-15",
            "checkout": "2025-07-18"
        },
        {
            "name": "Same-day booking",
            "checkin": "2025-06-30",
            "checkout": "2025-07-02"
        },
        {
            "name": "Long-term booking",
            "checkin": "2025-07-01",
            "checkout": "2025-08-01"
        },
        {
            "name": "Invalid past booking",
            "checkin": "2024-12-25",
            "checkout": "2024-12-26"
        }
    ]
    
    for scenario in scenarios:
        print(f"Scenario: {scenario['name']}")
        validation = validate_booking_dates(scenario['checkin'], scenario['checkout'])
        print(f"  Valid: {validation['valid']}")
        if validation.get('errors'):
            print(f"  Errors: {validation['errors']}")
        if validation.get('warnings'):
            print(f"  Warnings: {validation['warnings']}")
        print()


if __name__ == "__main__":
    test_time_utilities()
    test_booking_scenarios()
    print("✅ Time utility tests completed!") 