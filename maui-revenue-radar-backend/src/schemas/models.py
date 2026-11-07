from typing import Optional
from datetime import datetime, timedelta
from enum import Enum

class DemandClassification(Enum):
    EXCEPTIONAL = 120
    VERY_HIGH = (110, 120)
    HIGH = (103, 110)
    NORMAL = (97, 103)
    BELOW_NORMAL = (90, 97)
    WEAK = "below_90"

class OpportunityScore:
    def __init__(self, demand_index: float, classification: str):
        self.demand_index = demand_index
        self.classification = classification
    
    def get_classification(self) -> DemandClassification:
        if self.demand_index >= 120:
            return DemandClassification.EXCEPTIONAL
        elif self.demand_index >= 110:
            return DemandClassification.VERY_HIGH
        elif self.demand_index >= 103:
            return DemandClassification.HIGH
        elif self.demand_index >= 97:
            return DemandClassification.NORMAL
        elif self.demand_index >= 90:
            return DemandClassification.BELOW_NORMAL
        else:
            return DemandClassification.WEAK
    
    def get_color(self) -> str:
        if self.demand_index >= 120:
            return "#4CAF50"
        elif self.demand_index >= 110:
            return "#8BC34A"
        elif self.demand_index >= 103:
            return "#FFC107"
        elif self.demand_index >= 97:
            return "#BBBDBB"
        elif self.demand_index >= 90:
            return "#FFEB3B"
        else:
            return "#EF5350"

class DemandForecast:
    def __init__(self, 
                 date: datetime, 
                 predicted_arrivals: float,
                 confidence_range: dict):
        self.date = date
        self.predicted_arrivals = predicted_arrivals
        self.confidence_range = confidence_range
    
    def get_forecast_bounds(self) -> tuple:
        return (
            self.confidence_range["low"],
            self.confidence_range["high"]
        )

class RevenueScenario:
    def __init__(self, 
                 scenario_name: str,
                 expected_bookings: float,
                 gross_revenue: float,
                 operating_costs: float,
                 contribution_margin: float):
        self.scenario_name = scenario_name
        self.expected_bookings = expected_bookings
        self.gross_revenue = gross_revenue
        self.operating_costs = operating_costs
        self.contribution_margin = contribution_margin