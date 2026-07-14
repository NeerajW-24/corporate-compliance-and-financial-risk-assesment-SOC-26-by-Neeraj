# Corporate Compliance and Financial Risk Assessment

**Season of Code | WnCC, IIT Bombay [Mar'25]**

## Project Overview

A comprehensive system for detecting and monitoring trade-based money laundering (TBML) anomalies across 200+ economies using advanced statistical methods and data-driven analytics.

## Key Features

- **3 Integrated Public Datasets**: Streamlined trade compliance analytics covering 200+ economies using Python and SQL
- **6 TBML Typologies Detection**: Anomalous trade patterns identified using:
  - Benford's Law for invoice amount distributions
  - Mahalanobis Distance for multivariate outlier detection
  - Multivariate Regression for pattern analysis
- **12+ Compliance KPIs Dashboard**: Interactive Power BI dashboard for data-driven risk monitoring and anomaly detection

## Project Structure

```
soc'26/
├── data/                    # Dataset storage (3 public datasets)
├── src/                     # Source code modules
│   ├── data_integration/    # ETL pipeline for 200+ economies
│   ├── anomaly_detection/   # Benford's Law, Mahalanobis Distance
│   ├── tbml_detection/      # 6 TBML typologies
│   └── utils/               # Helper functions
├── sql/                     # SQL schemas and queries (200+ economies)
├── dashboard/               # Power BI configurations (12+ KPIs)
├── notebooks/               # Jupyter notebooks for analysis
├── config/                  # Configuration files
├── reports/                 # Generated reports and visualizations
├── requirements.txt         # Python dependencies
├── config.yaml              # Project configuration
└── main.py                  # Main application entry point
```

## Requirements

- Python 3.9+
- SQL Database (PostgreSQL/MySQL)
- Power BI Desktop (for dashboard)
- Libraries: pandas, numpy, scipy, scikit-learn, sqlalchemy, etc.

## Installation & Usage

See individual module documentation for detailed instructions.
