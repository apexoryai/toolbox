"""
Time utility functions for the hotel management toolbox.
Provides timezone-aware operations for booking validation and time-sensitive operations.
"""

from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
from typing import Optional, Tuple, Dict, Any
import pytz


def get_current_time(timezone: str = "America/Denver") -> Dict[str, Any]:
    """
    Get current time in specified timezone.
    
    Args:
        timezone: IANA timezone identifier (e.g., 'America/Denver', 'UTC')
        
    Returns:
        Dictionary with current time information
    """
    try:
        tz = ZoneInfo(timezone)
        now = datetime.now(tz)
        
        return {
            "timezone": timezone,
            "datetime": now.isoformat(),
            "date": now.date().isoformat(),
            "time": now.strftime("%H:%M:%S"),
            "is_dst": bool(now.dst()),
            "utc_offset": str(now.utcoffset()),
            "timestamp": now.timestamp()
        }
    except Exception as e:
        return {
            "error": f"Invalid timezone '{timezone}': {str(e)}",
            "available_timezones": list(pytz.all_timezones)[:10]  # First 10 as example
        }


def validate_booking_dates(checkin_date: str, checkout_date: str, 
                          timezone: str = "America/Denver") -> Dict[str, Any]:
    """
    Validate booking dates for hotel reservations.
    
    Args:
        checkin_date: Check-in date in YYYY-MM-DD format
        checkout_date: Check-out date in YYYY-MM-DD format
        timezone: Timezone for date validation
        
    Returns:
        Dictionary with validation results
    """
    try:
        # Parse dates
        checkin = datetime.strptime(checkin_date, "%Y-%m-%d").date()
        checkout = datetime.strptime(checkout_date, "%Y-%m-%d").date()
        
        # Get current date in specified timezone
        tz = ZoneInfo(timezone)
        current_date = datetime.now(tz).date()
        
        # Validation checks
        errors = []
        warnings = []
        
        if checkin < current_date:
            errors.append("Check-in date cannot be in the past")
        
        if checkin >= checkout:
            errors.append("Check-in date must be before check-out date")
        
        if checkin == current_date:
            warnings.append("Check-in is today - ensure hotel allows same-day check-in")
        
        # Calculate duration
        duration = (checkout - checkin).days
        
        if duration > 30:
            warnings.append(f"Long-term booking ({duration} days) - consider special rates")
        
        if duration < 1:
            errors.append("Booking duration must be at least 1 day")
        
        return {
            "valid": len(errors) == 0,
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
            "duration_days": duration,
            "current_date": current_date.isoformat(),
            "timezone": timezone,
            "errors": errors,
            "warnings": warnings
        }
        
    except ValueError as e:
        return {
            "valid": False,
            "error": f"Invalid date format: {str(e)}. Use YYYY-MM-DD format."
        }
    except Exception as e:
        return {
            "valid": False,
            "error": f"Validation error: {str(e)}"
        }


def convert_time_between_timezones(time_str: str, source_tz: str, target_tz: str) -> Dict[str, Any]:
    """
    Convert time between different timezones.
    
    Args:
        time_str: Time in HH:MM format (24-hour)
        source_tz: Source timezone (IANA identifier)
        target_tz: Target timezone (IANA identifier)
        
    Returns:
        Dictionary with converted time information
    """
    try:
        # Parse time
        time_obj = datetime.strptime(time_str, "%H:%M").time()
        
        # Get current date in source timezone
        source_zone = ZoneInfo(source_tz)
        target_zone = ZoneInfo(target_tz)
        
        # Create datetime with source timezone
        source_dt = datetime.now(source_zone).replace(
            hour=time_obj.hour, 
            minute=time_obj.minute, 
            second=0, 
            microsecond=0
        )
        
        # Convert to target timezone
        target_dt = source_dt.astimezone(target_zone)
        
        # Calculate time difference
        time_diff = target_dt.utcoffset() - source_dt.utcoffset()
        hours_diff = time_diff.total_seconds() / 3600
        
        return {
            "source_time": time_str,
            "source_timezone": source_tz,
            "target_time": target_dt.strftime("%H:%M"),
            "target_timezone": target_tz,
            "time_difference_hours": hours_diff,
            "formatted_difference": f"{hours_diff:+.1f}h"
        }
        
    except ValueError as e:
        return {
            "error": f"Invalid time format: {str(e)}. Use HH:MM format (24-hour)."
        }
    except Exception as e:
        return {
            "error": f"Conversion error: {str(e)}"
        }


def get_business_hours(timezone: str = "America/Denver") -> Dict[str, Any]:
    """
    Get business hours information for hotel operations.
    
    Args:
        timezone: Timezone for business hours
        
    Returns:
        Dictionary with business hours information
    """
    tz = ZoneInfo(timezone)
    now = datetime.now(tz)
    
    # Standard hotel business hours
    business_hours = {
        "checkin_start": "15:00",  # 3:00 PM
        "checkin_end": "23:59",    # Midnight
        "checkout_time": "11:00",  # 11:00 AM
        "front_desk_open": "06:00", # 6:00 AM
        "front_desk_close": "23:59" # Midnight
    }
    
    current_time = now.strftime("%H:%M")
    
    # Check if currently within business hours
    is_checkin_time = business_hours["checkin_start"] <= current_time <= business_hours["checkin_end"]
    is_front_desk_open = business_hours["front_desk_open"] <= current_time <= business_hours["front_desk_close"]
    
    return {
        "timezone": timezone,
        "current_time": current_time,
        "business_hours": business_hours,
        "is_checkin_time": is_checkin_time,
        "is_front_desk_open": is_front_desk_open,
        "next_checkin_start": business_hours["checkin_start"],
        "next_checkout_time": business_hours["checkout_time"]
    }


def format_duration(start_date: str, end_date: str) -> str:
    """
    Format booking duration in human-readable format.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        Formatted duration string
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        duration = (end - start).days
        
        if duration == 1:
            return "1 day"
        elif duration < 7:
            return f"{duration} days"
        elif duration < 30:
            weeks = duration // 7
            remaining_days = duration % 7
            if remaining_days == 0:
                return f"{weeks} week{'s' if weeks > 1 else ''}"
            else:
                return f"{weeks} week{'s' if weeks > 1 else ''} and {remaining_days} day{'s' if remaining_days > 1 else ''}"
        else:
            months = duration // 30
            remaining_days = duration % 30
            if remaining_days == 0:
                return f"{months} month{'s' if months > 1 else ''}"
            else:
                return f"{months} month{'s' if months > 1 else ''} and {remaining_days} day{'s' if remaining_days > 1 else ''}"
                
    except Exception:
        return "Invalid duration"


def get_timezone_abbreviation(timezone: str) -> str:
    """
    Get timezone abbreviation (e.g., MDT, PST, EST).
    
    Args:
        timezone: IANA timezone identifier
        
    Returns:
        Timezone abbreviation
    """
    try:
        tz = ZoneInfo(timezone)
        now = datetime.now(tz)
        return now.strftime("%Z")
    except Exception:
        return "Unknown"


# Common timezone mappings for user-friendly names
TIMEZONE_MAPPINGS = {
    "Mountain Time": "America/Denver",
    "Pacific Time": "America/Los_Angeles", 
    "Eastern Time": "America/New_York",
    "Central Time": "America/Chicago",
    "UTC": "UTC",
    "London": "Europe/London",
    "Paris": "Europe/Paris",
    "Tokyo": "Asia/Tokyo",
    "Sydney": "Australia/Sydney"
}


def resolve_timezone(timezone_input: str) -> str:
    """
    Resolve user-friendly timezone names to IANA identifiers.
    
    Args:
        timezone_input: User input (could be friendly name or IANA identifier)
        
    Returns:
        IANA timezone identifier
    """
    # Check if it's already an IANA identifier
    if timezone_input in pytz.all_timezones:
        return timezone_input
    
    # Check friendly mappings
    if timezone_input in TIMEZONE_MAPPINGS:
        return TIMEZONE_MAPPINGS[timezone_input]
    
    # Try to find partial matches
    for tz in pytz.all_timezones:
        if timezone_input.lower() in tz.lower():
            return tz
    
    # Default to UTC if no match found
    return "UTC" 