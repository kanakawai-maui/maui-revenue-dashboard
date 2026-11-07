from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI(title="Maui Revenue Radar - Tourism Demand Forecasting API")

# CORS configuration for Render deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DemandIndex:
    EXCEPTIONAL = 120.0
    VERY_HIGH = 115.0
    HIGH = 108.0
    NORMAL = 100.0
    BELOW_NORMAL = 94.0
    WEAK = 87.0

def calculate_demand_index(forecast_arrivals, expected_seasonal_arrivals):
    """Calculate demand index according to spec"""
    if expected_seasonal_arrivals == 0:
        return DemandIndex.NORMAL
    
    index = (forecast_arrivals / expected_seasonal_arrivals) * 100
    return round(index, 2)

def get_classification_label(index):
    """Return human-readable classification"""
    if index >= 120:
        return "Exceptional"
    elif index >= 110:
        return "Very High"
    elif index >= 103:
        return "High"
    elif index >= 97:
        return "Normal"
    elif index >= 90:
        return "Below Normal"
    else:
        return "Weak"

def get_color_by_class(index):
    """Get color for calendar visualization"""
    if index >= 120:
        return "#4CAF50"
    elif index >= 110:
        return "#8BC34A"
    elif index >= 103:
        return "#FFC107"
    elif index >= 97:
        return "#BBBDBB"
    elif index >= 90:
        return "#FFEB3B"
    else:
        return "#EF5350"

# API Endpoints
@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint for Render monitoring"""
    return {"status": "healthy", "service": "maui-revenue-radar"}

@app.get("/api/v1/dashboard")
async def get_dashboard_metrics(business_name: Optional[str] = None):
    """Business Intelligence Dashboard - core MVP feature"""

    # Simulate current demand
    dbedb_data = {"last_count": 8500, "previous_count": 7200}
    hta_forecast = {"scheduled_seats": 9500, "flight_count": 45}

    demand_index = calculate_demand_index(hta_forecast["scheduled_seats"], 7200)
    next_opportunity_days = [
        {"date": "2024-12-15", "classification": "High"},
        {"date": "2024-12-20", "classification": "Exceptional"},
        {"date": "2024-12-28", "classification": "Very High"},
    ]

    return {
        "business": business_name or "Unknown Business",
        "demand_status": get_classification_label(demand_index),
        "demand_index": demand_index,
        "next_opportunity_days": next_opportunity_days,
    }

@app.get("/api/v1/forecasts")
async def get_demand_forecast(horizon_days: int = 7, business_name: Optional[str] = None):
    """Demand forecasting with configurable horizon (7-90 days)"""
    
    return {
        "forecast_horizon": f"{horizon_days} days",
        "business": business_name or "Tour Operator",
        "forecasts": [
            {"day_offset": i, "predicted_arrivals": 8500 + (i * 200), "confidence_range": {
                "low": 6000 + (i * 100), 
                "high": 11000 + (i * 300)
            }}
            for i in range(1, horizon_days + 1)
        ]
    }

@app.get("/api/v1/calendar")
async def get_opportunity_calendar(days: int = 90):
    """Opportunity calendar - color-coded demand visualization"""
    
    return {
        "calendar_days": days,
        "forecast_dates": [
            {
                "date": f"2024-12-{i:02}", 
                "demand_index": round(100 + (i * 0.8), 1),
                "classification": get_classification_label(round(100 + (i * 0.8))),
                "color": get_color_by_class(round(100 + (i * 0.8)))
            }
            for i in range(1, days + 1)
        ]
    }

@app.post("/api/v1/revenue/simulate")
async def simulate_revenue_scenario(data: dict):
    """Business Revenue Simulator - configurable scenarios"""
    
    scenario = data.get("scenario", "baseline")
    adjustments = data.get("adjustments", {})
    
    base_booking_value = 150
    base_seats = 20
    base_departures = 3
    
    return {
        "simulated_scenario": scenario,
        "metrics": [
            {"name": "Expected Bookings", "value": round(base_seats * base_departures)},
            {"name": "Gross Revenue", "value": f"${round(base_seats * base_departures) * base_booking_value,0}"},
            {"name": "Operating Costs", "value": f"${round(base_seats * base_departures) * adjustments.get('cost_per_day', 2000)}"},
            {"name": "Contribution Margin", "value": f"${round((base_seats * base_departures) * base_booking_value - adjustments.get('cost_per_day', 2000))}"}
        ]
    }

@app.get("/api/v1/alerts")
async def get_alerts_configured():
    """Retrieved alerts for business"""
    return {
        "active_alerts": [
            {"type": "demand_increase", "message": "Maui demand forecast increased 12%", "severity": "high"},
            {"type": "opportunity_approaching", "message": "High-demand period approaching in 21 days", "severity": "medium"}
        ],
        "notification_preferences": ["email"]
    }

@app.get("/api/v1/alerts/preferences")
async def get_alert_preferences(alert_types: list, frequency_days: int = 7):
    """Configure alert preferences"""
    return {
        "configured_alerts": alert_types,
        "frequency_days": frequency_days,
        "channels": ["email"]
    }

@app.get("/api/v1/business/profile")
async def get_business_profile(data: dict):
    """Retrieve business profile configuration"""
    return {
        **data,
        "status": "active",
        "last_updated": datetime.now().isoformat()
    }

@app.post("/api/v1/bookings/import")
async def import_bookings(file_data: str):
    """Upload booking history (CSV/Excel)"""
    return {
        "status": "success",
        "message": "Booking data imported successfully",
        "record_count": 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
