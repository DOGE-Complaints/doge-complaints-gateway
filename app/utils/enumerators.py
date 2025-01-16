# Enumerators for dashboard lists

class ComplaintTimeType:
    EXACT = "exact"
    DATE = "date"
    DATE_RANGE = "date_range"
    DATETIME_RANGE = "datetime_range"
    TIME_INTERVAL = "time_interval"
    APPROX_PERIOD = "approx_period"

# Severity levels
SEVERITY_LEVELS = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

# Impact estimation
IMPACT_ESTIMATION = [
    "Personal",
    "City/Town",
    "State",
    "Country",
    "Earth"
]

# Problem status
PROBLEM_STATUS = [
    "Ongoing",
    "Resolved",
    "Worsened",
    "Pending Review"
]

# Time types
TIME_TYPES = [
    "Exact",
    "Date",
    "Date Range",
    "Datetime Range",
    "Time Interval",
    "Approximate Period"
]

# Media file types
MEDIA_FILE_TYPES = [
    "Image",
    "Video"
]
