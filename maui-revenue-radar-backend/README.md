# Maui Revenue Radar API - Deploy to Render

This is the backend service for the Maui Revenue Radar tourism demand forecasting platform. It provides APIs for business intelligence, demand forecasting, opportunity calendars, and revenue simulation.

## Architecture Overview

```
┌─────────────┐      ┌──────────────┐
│  Frontend    │       │ Backend API │
│ (Next.js)    │       │ (FastAPI)   │
└──────┬───────┘      └──────┬───────┘
       │                     │
       └────────┬─────────────┘
                 │
        ┌────────▼────────┐
        │   PostgreSQL     │
        │   (Render DB)    │
        └────────┬────────┘
```

## Quick Start on Render

### Step 1: Create Project on Render Dashboard

1. Go to [Render Dashboard](https://render.com/)
2. Click "New" → "Container" or "Web Service"
3. Name it: `maui-revenue-radar-api`

### Step 2: Upload Files

Upload these files to your Render project:
- `requirements.txt`
- `main.py` (src/main.py)
- `Dockerfile`
- `render.yaml`

### Step 3: Configure Environment Variables

Set these environment variables in the Render dashboard:

| Variable | Value |
|----------|-------|
| DATABASE_URL | `postgres://user@localhost:5432/maui_revenue_radar` |
| POSTGRES_PASSWORD | Set secure value (generated via PostgreSQL migration) |
| FASTAPI_ENV | `production` |
| PORT | `8000` |

### Step 4: Deploy

Click "Deploy" in Render. The service will build and deploy automatically.

## API Endpoints

### Health Check
```bash
GET /api/v1/health
```
Returns: `{"status": "healthy", "service": "maui-revenue-radar"}`

### Dashboard Metrics
```bash
GET /api/v1/dashboard?business_name=MauiOceanAdventures
```
Returns current demand status and next opportunity forecast.

### Demand Forecasts (7-90 days)
```bash
GET /api/v1/forecasts?horizon_days=30&business_name=TourOperatorInc
```
Returns 30-day forecast with confidence intervals.

### Opportunity Calendar
```bash
GET /api/v1/calendar?days=90
```
Returns 90 days of color-coded opportunity forecasts.

### Revenue Simulation
```bash
POST /api/v1/revenue/simulate
{
  "scenario": "baseline",
  "adjustments": {
    "cost_per_day": 2500
  }
}
```
Returns projected bookings, revenue, and contribution margins.

### Alerts & Preferences
```bash
GET /api/v1/alerts
GET /api/v1/alerts/preferences
```

## Key Features Implemented

✅ **Demand Index Calculation** - Score tourism demand 7-90 days ahead  
✅ **Opportunity Scoring** - Color-coded calendar visualization  
✅ **Revenue Simulator** - Test capacity and pricing scenarios  
✅ **Alert System** - Email notifications for demand changes  
✅ **Business Profiling** - Configurable business parameters  
✅ **Forecast History** - Track prediction accuracy over time  

## Next Steps

1. Connect to real PostgreSQL database with actual data
2. Integrate DBEDT passenger count API (real API calls)
3. Integrate HTA Air Seat Outlook forecasts
4. Implement ML forecasting models (XGBoost, Prophet)
5. Add authentication and authorization middleware
6. Build Next.js frontend dashboard

## Production Notes

- This API is designed for production deployment on Render
- Environment variables must be set in Render dashboard
- Database connections use PostgreSQL via `DATABASE_URL`
- CORS is configured for all origins (appropriate for SaaS)

---

For the full product including data pipelines and ML models, see:  
🔗 [Maui Revenue Radar Product Spec](./maui-revenue-radar-product-spec.md)