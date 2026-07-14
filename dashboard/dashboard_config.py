"""
Dashboard Configuration for Power BI
12+ Compliance KPIs Dashboard
"""

import json
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ComplianceKPI:
    """Represents a single KPI"""
    
    def __init__(self, kpi_id: int, name: str, description: str, 
                 unit: str, data_source: str):
        self.kpi_id = kpi_id
        self.name = name
        self.description = description
        self.unit = unit
        self.data_source = data_source
    
    def to_dict(self) -> Dict:
        return {
            'kpi_id': self.kpi_id,
            'name': self.name,
            'description': self.description,
            'unit': self.unit,
            'data_source': self.data_source
        }


class DashboardConfiguration:
    """
    Power BI Dashboard Configuration with 12+ KPIs
    """
    
    KPIS_COUNT = 12
    
    KPIS = [
        ComplianceKPI(1, "Total Transactions Monitored", 
                     "Total number of transactions analyzed in the period",
                     "Count", "trade_transactions"),
        ComplianceKPI(2, "Anomalies Detected (All Methods)",
                     "Total anomalies detected using all detection methods",
                     "Count", "anomaly_results"),
        ComplianceKPI(3, "High Risk Transactions",
                     "Transactions flagged as high risk or critical",
                     "Count", "anomaly_results"),
        ComplianceKPI(4, "Average Mahalanobis Distance",
                     "Average multivariate distance across transactions",
                     "Score", "anomaly_results"),
        ComplianceKPI(5, "Benford's Law Compliance %",
                     "Percentage of transactions complying with Benford's Law",
                     "Percentage", "anomaly_results"),
        ComplianceKPI(6, "Multivariate Regression Deviations",
                     "Number of transactions deviating from expected patterns",
                     "Count", "anomaly_results"),
        ComplianceKPI(7, "TBML Typology Distribution",
                     "Count of detected transactions per TBML typology",
                     "Distribution", "anomaly_results"),
        ComplianceKPI(8, "Economy-wise Risk Heatmap",
                     "Risk score distribution across 200+ economies",
                     "Map", "countries"),
        ComplianceKPI(9, "Temporal Trend Analysis",
                     "Anomaly trends over time periods",
                     "Trend", "anomaly_results"),
        ComplianceKPI(10, "Transaction Value Distribution",
                     "Distribution of transaction amounts analyzed",
                     "Distribution", "trade_transactions"),
        ComplianceKPI(11, "Flagged Entities",
                     "Number of unique exporters/importers flagged",
                     "Count", "risk_assessments"),
        ComplianceKPI(12, "Detection Accuracy",
                     "Percentage of accurately classified anomalies",
                     "Percentage", "anomaly_results"),
        ComplianceKPI(13, "False Positive Rate",
                     "Percentage of false positive detections",
                     "Percentage", "anomaly_results"),
        ComplianceKPI(14, "Risk Score Distribution",
                     "Distribution of risk scores across transactions",
                     "Distribution", "anomaly_results")
    ]
    
    def __init__(self):
        logger.info(f"Dashboard Configuration initialized with {self.KPIS_COUNT}+ KPIs")
    
    @staticmethod
    def get_all_kpis() -> List[Dict]:
        """Get all KPIs as dictionaries"""
        return [kpi.to_dict() for kpi in DashboardConfiguration.KPIS]
    
    @staticmethod
    def get_kpi_by_id(kpi_id: int) -> Dict:
        """Get specific KPI by ID"""
        for kpi in DashboardConfiguration.KPIS:
            if kpi.kpi_id == kpi_id:
                return kpi.to_dict()
        return None
    
    @staticmethod
    def get_dashboard_json() -> str:
        """
        Generate Power BI Dashboard configuration JSON
        """
        dashboard = {
            "name": "Corporate Compliance and Financial Risk Assessment Dashboard",
            "version": "1.0.0",
            "platform": "Power BI",
            "kpis_count": len(DashboardConfiguration.KPIS),
            "kpis": DashboardConfiguration.get_all_kpis(),
            "pages": [
                {
                    "page_id": 1,
                    "page_name": "Executive Summary",
                    "kpis": [1, 2, 3, 11],
                    "visualizations": ["KPI Cards", "Key Metrics"]
                },
                {
                    "page_id": 2,
                    "page_name": "Anomaly Detection",
                    "kpis": [4, 5, 6, 13],
                    "visualizations": ["Scatter Plot", "Heatmap", "Time Series"]
                },
                {
                    "page_id": 3,
                    "page_name": "TBML Analysis",
                    "kpis": [7, 9],
                    "visualizations": ["Pie Chart", "Trend Line", "Distribution"]
                },
                {
                    "page_id": 4,
                    "page_name": "Geographic Risk",
                    "kpis": [8],
                    "visualizations": ["World Map", "Heatmap", "Bar Chart"]
                },
                {
                    "page_id": 5,
                    "page_name": "Transaction Analysis",
                    "kpis": [10, 12, 14],
                    "visualizations": ["Histogram", "Box Plot", "Correlation Matrix"]
                }
            ],
            "data_connections": [
                {
                    "source": "SQL Database",
                    "tables": ["trade_transactions", "anomaly_results", "compliance_kpis", 
                             "countries", "tbml_typologies", "risk_assessments"]
                }
            ],
            "refresh_schedule": {
                "frequency": "daily",
                "time": "02:00 UTC"
            }
        }
        
        return json.dumps(dashboard, indent=2)
    
    @staticmethod
    def export_to_json(filepath: str):
        """Export dashboard configuration to JSON file"""
        with open(filepath, 'w') as f:
            f.write(DashboardConfiguration.get_dashboard_json())
        logger.info(f"Dashboard configuration exported to {filepath}")


# Example usage
if __name__ == "__main__":
    config = DashboardConfiguration()
    
    print("\n=== Power BI Dashboard KPIs (12+) ===")
    for kpi in DashboardConfiguration.KPIS:
        print(f"{kpi.kpi_id}. {kpi.name} - {kpi.description}")
    
    # Export configuration
    config.export_to_json('dashboard_config.json')
