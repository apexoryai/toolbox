from datetime import datetime
from zoneinfo import ZoneInfo

# Get current time in Mountain Daylight Time
mdt_tz = ZoneInfo("America/Denver")
current_time = datetime.now(mdt_tz)
print(f"Current time in MDT: {current_time}")
