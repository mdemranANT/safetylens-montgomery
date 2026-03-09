"""Configuration for SafetyLens Montgomery."""

# ─── Montgomery ArcGIS REST API Endpoints ───────────────────────────────────

ARCGIS_ONLINE_BASE = "https://services7.arcgis.com/xNUwUjOJqYE54USz/arcgis/rest/services"
GIS_SERVER_BASE = "https://gis.montgomeryal.gov/server/rest/services/HostedDatasets"

DATASETS = {
    "911_calls_monthly": {
        "url": f"{ARCGIS_ONLINE_BASE}/911_Calls_Data/FeatureServer/0",
        "description": "Monthly 911 call aggregates by category, origin, and phone service type.",
        "fields": ["Year", "Month", "Call_Category", "Phone_Service_Provider_Type",
                    "Call_Count_by_Phone_Service_Pro", "Call_Origin", "Call_Count_By_Origin"],
    },
    "911_calls_daily": {
        "url": f"{ARCGIS_ONLINE_BASE}/Emergency_911_Calls/FeatureServer/0",
        "description": "Daily emergency 911 call counts including inbound, outbound, admin, text.",
        "fields": ["Year", "Month", "Date", "F911_Inbound", "F911_Outbound",
                    "Admin_Inbound", "Admin_Outbound", "NENA", "Other",
                    "Text_Inbound", "Text_Outbound", "Total"],
    },
    "business_licenses": {
        "url": f"{GIS_SERVER_BASE}/Business_License/FeatureServer/0",
        "description": "Business licenses issued within the City of Montgomery.",
        "fields": [],  # dynamically discovered
    },
    "code_violations": {
        "url": f"{GIS_SERVER_BASE}/Code_Violations/FeatureServer/0",
        "description": "Code violation locations and details across the city.",
        "fields": [],
    },
    "311_requests": {
        "url": f"{GIS_SERVER_BASE}/Received_311_Service_Request/MapServer/0",
        "description": "311 service requests received by the City of Montgomery.",
        "fields": [],
    },
}

# ─── App Metadata ────────────────────────────────────────────────────────────

APP_TITLE = "SafetyLens Montgomery"
APP_SUBTITLE = "AI-Powered City Intelligence Platform"
APP_DESCRIPTION = (
    "An intelligent agent that analyzes Montgomery's public safety data, "
    "business licenses, code violations, and 311 requests — and compares "
    "real city data with public news perception using Bright Data."
)

CHALLENGE_AREAS = [
    "Public Safety, Emergency Response & City Analytics",
    "Civic Access & Community Communication",
    "Workforce, Business & Economic Growth",
    "Smart Cities, Infrastructure & Public Spaces",
]
