# Corporate Compliance and Financial Risk Assessment
# Setup and Execution Guide

## Project Overview

This is a comprehensive system for detecting and monitoring Trade-Based Money Laundering (TBML) anomalies across 200+ economies using advanced statistical methods and data-driven analytics.

### Key Components

**3 Integrated Datasets:**
- UN Comtrade Database
- World Bank Trade Statistics  
- IMF Direction of Trade Statistics (DOTS)

**3 Anomaly Detection Methods:**
- Benford's Law (invoice amount distribution)
- Mahalanobis Distance (multivariate outlier detection)
- Multivariate Regression (pattern analysis)

**6 TBML Typologies:**
1. Over-invoicing
2. Under-invoicing
3. Over-shipment
4. Under-shipment
5. Phantom Shipment
6. Misclassification

**12+ Compliance KPIs Dashboard:**
- Total Transactions Monitored
- Anomalies Detected (All Methods)
- High Risk Transactions
- Average Mahalanobis Distance
- Benford's Law Compliance %
- Multivariate Regression Deviations
- TBML Typology Distribution
- Economy-wise Risk Heatmap (200+ economies)
- Temporal Trend Analysis
- Transaction Value Distribution
- Flagged Entities
- Detection Accuracy
- False Positive Rate
- Risk Score Distribution

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL or MySQL
- Git

### Steps

1. **Clone Repository**
   ```bash
   cd /Users/neeraj/Documents/soc'26
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**
   - Update `config/config.yaml` with your database credentials
   - Create database and run schema:
   ```bash
   psql -U postgres -f sql/schema_economies.sql
   ```

5. **Run Application**
   ```bash
   python main.py --stage all
   ```

## Usage

### Run Full Pipeline
```bash
python main.py --stage all
```

### Run Specific Stage
```bash
python main.py --stage 1  # Data Integration
python main.py --stage 2  # Anomaly Detection
python main.py --stage 3  # TBML Detection
python main.py --stage 4  # Dashboard Configuration
```

### Jupyter Notebooks
```bash
jupyter notebook notebooks/
```

## Project Structure

```
soc'26/
├── data/                      # Raw datasets
├── src/
│   ├── data_integration.py    # 3 datasets, 200+ economies
│   ├── anomaly_detection.py   # 3 detection methods
│   ├── tbml_detection.py      # 6 typologies
│   ├── utils.py               # Helper functions
│   └── __init__.py
├── sql/
│   ├── schema_economies.sql   # Database schema (200+ economies)
│   └── dashboard_kpis.sql     # 12+ KPI queries
├── dashboard/
│   └── dashboard_config.py    # Power BI configuration
├── notebooks/
│   ├── 01_data_integration.ipynb
│   ├── 02_anomaly_detection.ipynb
│   └── 03_tbml_detection.ipynb
├── config/
│   └── config.yaml            # Configuration file
├── reports/                   # Generated reports
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
└── README.md
```

## Configuration

Edit `config/config.yaml` to customize:
- Database connection
- Detection thresholds
- TBML parameters
- Dashboard settings

## Database Schema

The schema supports:
- **200+ Countries** with AML risk ratings
- **3 Dataset Sources** with unified structure
- **6 TBML Typologies** detection
- **14 Dashboard KPIs**
- Comprehensive audit logging

## Output

- **Logs**: `logs/compliance_analysis.log`
- **Reports**: `reports/` directory
- **Database**: SQL tables with complete analysis
- **Dashboard**: Power BI visualizations

## Performance

- Processes 4,500+ transactions per stage
- 200+ economy coverage
- Real-time anomaly detection
- Scalable architecture

## Team

Season of Code | WnCC, IIT Bombay [Mar'25]

## License

Proprietary - All Rights Reserved
