I've formatted the specification as a Markdown document that you can copy into a file named:

`maui-revenue-radar-product-spec.md`

Writing

# Maui Revenue Radar

## Product Requirements & Technical Specification

**Version:** 1.0\
**Product type:** Tourism Intelligence SaaS\
**Initial market:** Maui, Hawaii\
**Primary customers:** Tour operators, boat charters, and activity providers\
**Core objective:** Forecast tourism demand and identify periods of high revenue opportunity.

---

# 1\. Product Vision

Maui Revenue Radar is a subscription-based tourism intelligence platform that helps tourism businesses anticipate demand, identify revenue opportunities, and make better operational decisions.

The platform combines two public data sources:

1. Hawaii DBEDT Daily Passenger Counts.
2. Hawaii Tourism Authority Air Seat Outlook.

It uses historical tourism patterns and forward-looking airline capacity to predict tourism demand 7–90 days ahead.

The platform translates these predictions into business-specific insights, helping customers optimize staffing, capacity, marketing, and revenue.

## Core value proposition

Know when tourism demand is likely to increase before it happens.

## Primary questions the product answers

- When will customer demand be unusually high?
- How far in advance should a business prepare?
- How much revenue could potentially be generated?
- When should businesses add capacity or staff?
- When is demand likely to weaken?
- What actions could improve business performance?

# 2\. Target Customers

## Primary market

Tour operators and activity providers.

Examples:

- Boat charter companies.
- Snorkeling operators.
- Whale-watching operators.
- Guided adventure companies.
- Surf schools.
- Zipline operators.
- Equipment rental companies.

## Secondary markets

- Restaurants.
- Vacation rental operators.
- Hotels.
- Transportation companies.
- Hospitality businesses.

## Why tour operators first?

Tour operators have limited inventory, fixed departure times, finite capacity, and perishable inventory.

An empty boat seat represents lost potential revenue.

This makes the value proposition measurable.

# 3\. Data Sources

The MVP should use two primary public data sources.

## Source A: Hawaii DBEDT Daily Passenger Counts

URL: [https://dbedt.hawaii.gov/visitor/daily-passenger-counts/](<https://dbedt.hawaii.gov/visitor/daily-passenger-counts/>)

Purpose: Historical tourism demand.

Required fields:

| Field | Description |
| --- | --- |
| arrival\_date | Date of arrival |
| island | Destination island |
| passenger\_count | Published passenger count |
| reporting\_period | Reporting frequency |
| source\_updated\_at | Source publication/update date |
| source\_reference | Original report |
| ingested\_at | Platform ingestion timestamp |

Requirements:

- Import historical observations.
- Preserve original source files.
- Normalize dates and island names.
- Detect revised historical values.
- Store source timestamps.
- Run scheduled ingestion.
- Flag missing or delayed reports.

Important: Passenger counts must not automatically be treated as unique tourists. Preserve the source metric definitions.

## Source B: Hawaii Tourism Authority Air Seat Outlook

URL: [https://hta.hawaii.gov/research/](<https://hta.hawaii.gov/research/>)

Purpose: Forward-looking airline capacity.

Required fields:

| Field | Description |
| --- | --- |
| forecast\_date | Date the outlook was published |
| travel\_period | Future travel period |
| origin\_region | Origin market |
| destination | Maui or other island |
| scheduled\_seats | Forecast seat capacity |
| scheduled\_flights | Flight count, if available |
| source\_updated\_at | Publication date |
| source\_reference | Original report |

Requirements:

- Import published airline capacity forecasts.
- Preserve historical forecast versions.
- Track changes between publications.
- Maintain original reporting granularity.
- Avoid inventing daily seat estimates from weekly or monthly totals.

Historical forecast versions are particularly valuable because they allow the model to learn how airline capacity changes as travel dates approach.

# 4\. Data Architecture

Recommended architecture:

text

```text
DBEDT + HTA
     |
     v
Python Ingestion Services
     |
     v
Data Validation and Normalization
     |
     v
PostgreSQL Database
     |
     v
Forecasting Engine
     |
     v
Opportunity Scoring
     |
     v
FastAPI Backend
     |
     v
Next.js Dashboard
     |
     v
Customer Applications
```

## Database

Use PostgreSQL initially.

Recommended tables:

| Table | Purpose |
| --- | --- |
| users | User accounts |
| organizations | Subscriber businesses |
| business\_profiles | Business operating details |
| data\_sources | External source registry |
| source\_observations | Raw imported records |
| passenger\_arrivals | Historical DBEDT data |
| air\_seat\_forecasts | HTA capacity forecasts |
| forecast\_runs | Model execution history |
| demand\_forecasts | Predicted tourism demand |
| opportunity\_scores | Daily opportunity classifications |
| business\_capacity | Business inventory |
| booking\_history | Customer booking uploads |
| revenue\_forecasts | Personalized revenue projections |
| alerts | Customer notifications |
| subscriptions | Billing information |

Important database requirements:

- Preserve historical forecasts.
- Track data provenance.
- Store model versions.
- Separate public and private data.
- Support multiple geographic levels.
- Maintain source reporting granularity.

# 5\. Forecasting Engine

The forecasting engine is the core technology.

It should have three layers.

## Layer 1: Tourism Demand Forecast

Predict total Maui tourism demand.

Inputs:

- Historical passenger counts.
- Seasonal patterns.
- Day of week.
- Month of year.
- Scheduled airline capacity.
- Historical differences between scheduled and actual arrivals.

Outputs:

- Expected daily arrivals, where data supports daily resolution.
- Expected weekly arrivals.
- Forecast uncertainty.
- Demand relative to seasonal baseline.

## Layer 2: Tourism Opportunity Score

Calculate:

text

```text
Demand Index =
(Forecast Arrivals / Expected Seasonal Arrivals) * 100
```

Initial proposed classifications:

| Demand Index | Classification |
| --- | --- |
| 120+ | Exceptional |
| 110–119 | Very high |
| 103–109 | High |
| 97–102 | Normal |
| 90–96 | Below normal |
| Below 90 | Weak |

These thresholds must be calibrated using historical data.

Each forecast must also display uncertainty and confidence.

## Layer 3: Business-Specific Revenue Forecast

Translate market demand into potential customer revenue.

For example:

text

```text
Expected Revenue =
Expected Bookings * Average Booking Value
```

And:

text

```text
Expected Bookings =
Available Seats * Expected Occupancy
```

Allow customers to configure:

- Daily departures.
- Seats per departure.
- Average ticket price.
- Operating costs.
- Historical bookings.
- Operating days.

Do not equate market-wide visitor demand with revenue captured by an individual business.

# 6\. Application Screens

The application should have six primary screens.

## Screen 1: Business Intelligence Dashboard

Purpose: Show the customer upcoming opportunities immediately.

Components:

- Tourism demand index.
- Next 30 days.
- Next 90 days.
- Revenue opportunity.
- Upcoming alerts.
- Forecast confidence.
- Demand trend charts.

Primary headline example:

"Your next high-demand opportunity is projected for December 18–22."

All dates and predictions must be dynamically generated.

## Screen 2: Revenue Opportunity Calendar

Display the next 90 days in a color-coded calendar.

- Green: Above-normal demand.
- Yellow: Normal demand.
- Red: Below-normal demand.
- Grey: Insufficient data.

Each date should include:

- Demand index.
- Forecast arrivals, where supported.
- Expected business occupancy, if configured.
- Estimated revenue, if sufficient data exists.
- Forecast confidence.

Clicking a date opens a detailed opportunity panel.

## Screen 3: Demand Forecasting

Provide selectable forecast horizons:

- 7 days.
- 14 days.
- 30 days.
- 60 days.
- 90 days.

Display:

- Historical actuals.
- Predicted demand.
- Seasonal baseline.
- Upper and lower forecast bounds.
- Year-over-year comparison.

## Screen 4: Business Revenue Simulator

Allow users to simulate:

- Adding another tour departure.
- Increasing ticket prices.
- Increasing available capacity.
- Reducing capacity.
- Changes in occupancy.
- Advertising campaigns.

Calculate:

- Expected bookings.
- Gross revenue.
- Operating expenses.
- Contribution margin.
- Differences between scenarios.

Clearly distinguish estimated outcomes from guaranteed revenue.

## Screen 5: Alerts and Opportunities

Provide automated alerts.

Examples:

- Maui demand forecast increased 12%.
- High-demand period approaching in 21 days.
- Configured business capacity may be insufficient.
- Airline capacity outlook changed materially.
- Forecast confidence decreased.

Delivery methods:

- Email.
- In-app notifications.
- SMS in a later version.

Users can configure thresholds and frequency.

## Screen 6: Business Settings

Business onboarding fields:

| Field | Example |
| --- | --- |
| Business name | Maui Ocean Adventures |
| Category | Boat tours |
| Location | Maalaea |
| Operating days | Monday–Sunday |
| Daily departures | 3 |
| Seats per departure | 20 |
| Average booking price | $150 |
| Average operating cost | $2,000/day |
| Historical bookings | Optional upload |
| Alert preferences | Email |

# 7\. Technical Architecture

Recommended stack:

| Component | Technology |
| --- | --- |
| Frontend | Next.js |
| Language | TypeScript |
| Backend | Python + FastAPI |
| Database | PostgreSQL |
| Geospatial | PostGIS |
| Forecasting | Python + XGBoost |
| Visualization | Recharts |
| UI styling | Tailwind CSS |
| Authentication | Supabase Auth |
| Payments | Stripe |
| Hosting | AWS or Render |
| Background jobs | Celery or managed scheduler |
| Monitoring | Sentry |
| Object storage | S3-compatible storage |

Keep the application logic and forecasting independent of individual hosting providers.

## API Endpoints

| Endpoint | Method | Purpose |
| --- | --- | --- |
| /api/v1/dashboard | GET | Dashboard metrics |
| /api/v1/demand | GET | Historical demand |
| /api/v1/forecasts | GET | Demand forecasts |
| /api/v1/calendar | GET | Opportunity calendar |
| /api/v1/revenue/simulate | POST | Revenue simulation |
| /api/v1/business/profile | GET/PUT | Business settings |
| /api/v1/bookings/import | POST | Booking upload |
| /api/v1/alerts | GET | Notifications |
| /api/v1/alerts/preferences | PUT | Alert preferences |

All endpoints must enforce organization-level authorization.

# 8\. Forecasting Model Development

Start with a simple seasonal baseline.

Then evaluate:

- Seasonal ARIMA.
- Exponential smoothing.
- Prophet.
- XGBoost regression.

Introduce scheduled airline seat capacity as an explanatory variable.

Eventually develop separate customer-specific models for different tourism business categories.

## Validation metrics

| Metric | Purpose |
| --- | --- |
| MAE | Average absolute forecast error |
| WAPE | Weighted percentage error |
| Bias | Overprediction or underprediction |
| Prediction interval coverage | Forecast uncertainty calibration |
| Revenue forecast error | Predicted versus actual revenue |

Use rolling historical backtesting.

Only use information that would have been available at the historical forecast date.

The forecasting engine must outperform a simple seasonal baseline before its predictions are marketed as superior.

# 9\. Subscription Business Model

Proposed pricing for initial testing:

## Free

$0/month

- Basic tourism demand index.
- 7-day outlook.
- Limited dashboard.
- Weekly email summary.

## Professional

$49/month

- 30-day forecasts.
- 90-day outlook.
- Opportunity calendar.
- Email alerts.
- Demand comparisons.

## Business

$149/month

- Everything in Professional.
- Business-specific forecasts.
- Revenue simulator.
- Historical booking uploads.
- Custom alert thresholds.
- Multiple users.

## Enterprise

$299+/month

- Multiple locations.
- Custom reporting.
- Team management.
- Priority support.
- API access, depending on plan.

These are proposed prices that require willingness-to-pay validation.

## Illustrative recurring revenue

| Subscribers | Monthly revenue at $149 |
| --- | --- |
| 25 | $3,725 |
| 50 | $7,450 |
| 100 | $14,900 |
| 250 | $37,250 |
| 500 | $74,500 |

Revenue is gross subscription revenue before expenses, taxes, refunds, and churn.

# 10\. Security and Compliance

Requirements:

- TLS encryption.
- Encryption at rest.
- Role-based access controls.
- Organization-level data isolation.
- Secure authentication.
- Automated backups.
- Audit logs.
- Data export and deletion processes.
- Explicit consent for booking-data uploads.
- Documented source licensing and attribution.
- Privacy policy and terms of service.

Customers retain ownership of their underlying booking data.

The company receives permission to process it to provide the service.

Do not expose identifiable customer booking data to other subscribers.

# 11\. Development Roadmap

Target: 8–10 weeks.

| Phase | Duration | Deliverable |
| --- | --- | --- |
| Product design | Week 1 | Wireframes and database design |
| Data ingestion | Weeks 2–3 | DBEDT and HTA pipelines |
| Forecasting | Weeks 3–4 | Initial demand model |
| Dashboard | Weeks 4–5 | Application screens |
| Business profiles | Week 6 | Customer onboarding |
| Revenue simulator | Week 7 | Personalized scenarios |
| Billing and alerts | Week 8 | Subscription functionality |
| Testing | Weeks 9–10 | Pilot-ready application |

# 12\. Estimated Development Budget

| Approach | Estimated cost |
| --- | --- |
| AI-assisted founder development | $500–$2,500 |
| Freelance developer | $5,000–$15,000 |
| Professional MVP | $15,000–$30,000 |
| More complete commercial product | $30,000–$60,000+ |

These are planning estimates, not vendor quotes.

# 13\. MVP Acceptance Criteria

Before launch:

- [ ]DBEDT historical data imported.
- [ ]HTA airline seat outlook imported.
- [ ]Source timestamps preserved.
- [ ]Forecast history retained.
- [ ]Daily and weekly forecasts generated.
- [ ]Forecast uncertainty displayed.
- [ ]Forecasts outperform seasonal baseline.
- [ ]90-day opportunity calendar operational.
- [ ]Business profiles functional.
- [ ]Capacity and pricing configurable.
- [ ]Revenue simulator operational.
- [ ]Email alerts functional.
- [ ]Subscription billing operational.
- [ ]Organization-level data isolation tested.
- [ ]Mobile-responsive application.

# 14\. Excluded from MVP

Avoid scope creep.

Do not initially build:

- AI chatbot.
- Native mobile applications.
- Global tourism coverage.
- Live flight tracking.
- Hotel booking integrations.
- Automated price changes.
- Social media sentiment analysis.
- Competitor scraping.
- Complex AI agents.
- GPU infrastructure.
- Extensive third-party integrations.

# 15\. Long-Term Competitive Advantage

The public datasets are not a competitive moat.

The moat should develop through:

1. Forecasting history: A record of predictions and actual outcomes.
2. Business-specific intelligence: Permissioned booking and capacity data.
3. Tourism expertise: Understanding how island-wide demand translates into commercial purchasing behavior.
4. Customer relationships: Becoming part of the operator's regular planning process.
5. Forecast accuracy: Demonstrably improving prediction performance over time.

Long-term geographic expansion:

- Maui.
- Oahu.
- Kauai.
- Hawaii Island.
- Other island tourism markets.
- International tourism destinations.

# 16\. Development Priorities

Build the product in two major components.

## Component A: Maui Tourism Demand Engine

Build first.

- Public data ingestion.
- Historical database.
- Demand forecasting.
- Forecast validation.
- Opportunity scoring.
- Forecast history.

This is the technical foundation.

## Component B: Maui Revenue Radar

Build second.

- Business accounts.
- Revenue dashboards.
- Opportunity calendar.
- Revenue simulator.
- Alerts.
- Subscription billing.

This is the commercial application customers pay for.

# 17\. Developer Implementation Brief

**Project:** Maui Revenue Radar

**Product:** Multi-tenant subscription SaaS.

**Primary user:** Maui tour and activity business owners.

**Core functionality:** Forecast tourism demand 7–90 days ahead using DBEDT daily passenger arrivals and HTA airline seat outlook data.

**Value proposition:** Identify high-opportunity periods and help tourism operators make better capacity, staffing, marketing, and revenue decisions.

**Frontend:** Next.js, TypeScript, Tailwind CSS, Recharts.

**Backend:** Python, FastAPI.

**Database:** PostgreSQL.

**Forecasting:** Seasonal baseline, XGBoost, forecast uncertainty, historical backtesting.

**Authentication:** Supabase Auth.

**Billing:** Stripe.

**Initial geography:** Maui.

**Initial customers:** Boat charters, tour operators, and activity businesses.

**Primary screens:** Dashboard, opportunity calendar, forecasting, revenue simulator, alerts, business settings.

**Primary data sources:**

- [https://dbedt.hawaii.gov/visitor/daily-passenger-counts/](<https://dbedt.hawaii.gov/visitor/daily-passenger-counts/>)
- [https://hta.hawaii.gov/research/](<https://hta.hawaii.gov/research/>)

**Design direction:** Premium financial analytics SaaS. Clean, sophisticated, data-dense, mobile-responsive. Navy, charcoal, muted green, and neutral grey. Avoid generic tourism website aesthetics.

**Development priority:** Build data ingestion and historical forecasting before polishing the dashboard.

**Data integrity requirement:** Never display synthetic or unverified figures as actual forecasts.

---

## Final Product Principle

Maui Revenue Radar should not be another tourism statistics website.

It should become an operational intelligence tool that helps tourism businesses make better decisions before demand arrives.

The first milestone is proving that two public datasets can generate useful, validated 30–90-day demand forecasts.

The second milestone is demonstrating that those forecasts help a real Maui tourism business improve its revenue decisions.

The third milestone is converting those results into a repeatable subscription business.

You can copy the document into a text editor and save it as `maui-revenue-radar-product-spec.md`.