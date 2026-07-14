-- SQL Schema for 200+ Economies Trade Compliance Database
-- Total Economies: 200+
-- Designed for trade compliance and anomaly detection

-- Countries Table (200+ economies)
CREATE TABLE IF NOT EXISTS countries (
    country_id SERIAL PRIMARY KEY,
    country_code VARCHAR(3) UNIQUE NOT NULL,
    country_name VARCHAR(255) NOT NULL,
    region VARCHAR(100),
    sub_region VARCHAR(100),
    income_level VARCHAR(50),
    aml_risk_rating VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trade Partners Table (for bilateral trade analysis)
CREATE TABLE IF NOT EXISTS trade_partners (
    partner_id SERIAL PRIMARY KEY,
    exporter_country_id INT NOT NULL REFERENCES countries(country_id),
    importer_country_id INT NOT NULL REFERENCES countries(country_id),
    trade_volume_annual DECIMAL(20, 2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_partner_pair UNIQUE(exporter_country_id, importer_country_id)
);

-- Commodities/HS Codes Table
CREATE TABLE IF NOT EXISTS commodities (
    commodity_id SERIAL PRIMARY KEY,
    hs_code VARCHAR(6) UNIQUE NOT NULL,
    commodity_description VARCHAR(500),
    commodity_group VARCHAR(100),
    risk_flag BOOLEAN DEFAULT FALSE,
    is_sensitive BOOLEAN DEFAULT FALSE
);

-- Trade Transactions Table (Dataset 1: UN Comtrade)
CREATE TABLE IF NOT EXISTS trade_transactions (
    transaction_id BIGSERIAL PRIMARY KEY,
    transaction_date DATE NOT NULL,
    exporter_country_id INT NOT NULL REFERENCES countries(country_id),
    importer_country_id INT NOT NULL REFERENCES importer_countries(country_id),
    commodity_id INT NOT NULL REFERENCES commodities(commodity_id),
    quantity DECIMAL(20, 4),
    quantity_unit VARCHAR(10),
    invoice_amount DECIMAL(20, 2) NOT NULL,
    reported_amount DECIMAL(20, 2),
    unit_price DECIMAL(15, 4),
    transaction_type VARCHAR(50),
    dataset_source VARCHAR(50) DEFAULT 'UN_COMTRADE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_amount CHECK (invoice_amount > 0)
);

-- World Bank Trade Data Table (Dataset 2)
CREATE TABLE IF NOT EXISTS wb_trade_statistics (
    wb_record_id BIGSERIAL PRIMARY KEY,
    wb_transaction_date DATE NOT NULL,
    exporter_country_id INT NOT NULL REFERENCES countries(country_id),
    importer_country_id INT NOT NULL REFERENCES countries(country_id),
    commodity_id INT NOT NULL REFERENCES commodities(commodity_id),
    trade_value DECIMAL(20, 2),
    trade_percentage DECIMAL(5, 2),
    dataset_source VARCHAR(50) DEFAULT 'WORLD_BANK',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- IMF DOTS Data Table (Dataset 3)
CREATE TABLE IF NOT EXISTS imf_dots_statistics (
    imf_record_id BIGSERIAL PRIMARY KEY,
    imf_transaction_date DATE NOT NULL,
    exporter_country_id INT NOT NULL REFERENCES countries(country_id),
    importer_country_id INT NOT NULL REFERENCES countries(country_id),
    commodity_id INT NOT NULL REFERENCES commodities(commodity_id),
    trade_value DECIMAL(20, 2),
    growth_rate DECIMAL(5, 2),
    dataset_source VARCHAR(50) DEFAULT 'IMF_DOTS',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Importer Countries Reference (for clarity)
CREATE TABLE IF NOT EXISTS importer_countries (
    country_id SERIAL PRIMARY KEY,
    country_code VARCHAR(3) UNIQUE NOT NULL REFERENCES countries(country_code),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TBML Typologies Table (6 typologies)
CREATE TABLE IF NOT EXISTS tbml_typologies (
    typology_id SERIAL PRIMARY KEY,
    typology_name VARCHAR(100) NOT NULL UNIQUE,
    typology_description TEXT,
    risk_level VARCHAR(20),
    typical_amount_range VARCHAR(50),
    typical_goods_category VARCHAR(100)
);

-- Anomaly Detection Results
CREATE TABLE IF NOT EXISTS anomaly_results (
    anomaly_id BIGSERIAL PRIMARY KEY,
    transaction_id BIGINT REFERENCES trade_transactions(transaction_id),
    detection_method VARCHAR(100),
    benford_law_score DECIMAL(5, 4),
    mahalanobis_distance DECIMAL(10, 4),
    multivariate_deviation DECIMAL(5, 4),
    tbml_typology_id INT REFERENCES tbml_typologies(typology_id),
    anomaly_score DECIMAL(5, 4),
    is_flagged BOOLEAN DEFAULT FALSE,
    detection_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    risk_classification VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Compliance KPIs Table (12+ KPIs)
CREATE TABLE IF NOT EXISTS compliance_kpis (
    kpi_id SERIAL PRIMARY KEY,
    kpi_date DATE NOT NULL,
    total_transactions_monitored BIGINT,
    anomalies_detected INT,
    high_risk_transactions INT,
    avg_mahalanobis_distance DECIMAL(10, 4),
    benford_law_compliance_pct DECIMAL(5, 2),
    multivariate_deviations INT,
    tbml_typology_count INT,
    flagged_entities INT,
    false_positive_rate DECIMAL(5, 2),
    detection_accuracy DECIMAL(5, 2),
    avg_risk_score DECIMAL(5, 4),
    transaction_value_sum DECIMAL(20, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_kpi_date UNIQUE(kpi_date)
);

-- Risk Assessment Table
CREATE TABLE IF NOT EXISTS risk_assessments (
    assessment_id BIGSERIAL PRIMARY KEY,
    entity_country_id INT REFERENCES countries(country_id),
    assessment_date DATE NOT NULL,
    overall_risk_score DECIMAL(5, 4),
    aml_risk_flag BOOLEAN,
    recommendation VARCHAR(255),
    assessed_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit Log Table
CREATE TABLE IF NOT EXISTS audit_log (
    log_id BIGSERIAL PRIMARY KEY,
    action VARCHAR(100),
    user_name VARCHAR(100),
    entity_affected VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT
);

-- Create Indexes for Performance
CREATE INDEX idx_transaction_date ON trade_transactions(transaction_date);
CREATE INDEX idx_country_on_transactions ON trade_transactions(exporter_country_id, importer_country_id);
CREATE INDEX idx_anomaly_flag ON anomaly_results(is_flagged);
CREATE INDEX idx_kpi_date ON compliance_kpis(kpi_date);
CREATE INDEX idx_risk_score ON anomaly_results(anomaly_score);
CREATE INDEX idx_typology_transactions ON anomaly_results(tbml_typology_id);

-- Create Views for Dashboard
CREATE VIEW v_high_risk_transactions AS
SELECT 
    t.transaction_id,
    c_exp.country_name as exporter,
    c_imp.country_name as importer,
    t.invoice_amount,
    ar.anomaly_score,
    ar.risk_classification,
    t.transaction_date
FROM trade_transactions t
JOIN countries c_exp ON t.exporter_country_id = c_exp.country_id
JOIN countries c_imp ON t.importer_country_id = c_imp.country_id
JOIN anomaly_results ar ON t.transaction_id = ar.transaction_id
WHERE ar.is_flagged = TRUE
ORDER BY ar.anomaly_score DESC;

CREATE VIEW v_economy_risk_heatmap AS
SELECT 
    c.country_code,
    c.country_name,
    COUNT(ar.anomaly_id) as anomaly_count,
    AVG(ar.anomaly_score) as avg_risk_score,
    SUM(CASE WHEN ar.is_flagged THEN 1 ELSE 0 END) as flagged_count
FROM countries c
LEFT JOIN trade_transactions t ON c.country_id = t.exporter_country_id
LEFT JOIN anomaly_results ar ON t.transaction_id = ar.transaction_id
GROUP BY c.country_id, c.country_code, c.country_name
ORDER BY avg_risk_score DESC;
