-- Queries for Dashboard KPIs
-- These SQL queries populate the 12+ KPIs in Power BI Dashboard

-- Query 1: Total Transactions Monitored
SELECT COUNT(*) as total_transactions
FROM trade_transactions;

-- Query 2: Anomalies Detected (All Methods)
SELECT COUNT(*) as total_anomalies
FROM anomaly_results
WHERE is_flagged = TRUE;

-- Query 3: High Risk Transactions
SELECT COUNT(*) as high_risk_transactions
FROM anomaly_results
WHERE risk_classification IN ('HIGH', 'CRITICAL');

-- Query 4: Average Mahalanobis Distance
SELECT AVG(mahalanobis_distance) as avg_mahalanobis_distance
FROM anomaly_results;

-- Query 5: Benford's Law Compliance %
SELECT 
    COUNT(CASE WHEN benford_law_score > 0.85 THEN 1 END) * 100.0 / COUNT(*) as compliance_percentage
FROM anomaly_results;

-- Query 6: Multivariate Regression Deviations
SELECT COUNT(*) as multivariate_deviations
FROM anomaly_results
WHERE multivariate_deviation > 0.5;

-- Query 7: TBML Typology Distribution
SELECT 
    tt.typology_name,
    COUNT(ar.anomaly_id) as count,
    tt.risk_level
FROM anomaly_results ar
LEFT JOIN tbml_typologies tt ON ar.tbml_typology_id = tt.typology_id
GROUP BY tt.typology_name, tt.risk_level
ORDER BY count DESC;

-- Query 8: Economy-wise Risk Heatmap (200+ economies)
SELECT 
    c.country_code,
    c.country_name,
    COUNT(ar.anomaly_id) as anomaly_count,
    AVG(ar.anomaly_score) as avg_risk_score
FROM countries c
LEFT JOIN trade_transactions t ON c.country_id = t.exporter_country_id
LEFT JOIN anomaly_results ar ON t.transaction_id = ar.transaction_id
GROUP BY c.country_id, c.country_code, c.country_name
ORDER BY avg_risk_score DESC;

-- Query 9: Temporal Trend Analysis
SELECT 
    DATE_TRUNC('month', t.transaction_date) as month,
    COUNT(ar.anomaly_id) as anomalies,
    AVG(ar.anomaly_score) as avg_risk
FROM trade_transactions t
LEFT JOIN anomaly_results ar ON t.transaction_id = ar.transaction_id
GROUP BY DATE_TRUNC('month', t.transaction_date)
ORDER BY month;

-- Query 10: Transaction Value Distribution
SELECT 
    CASE 
        WHEN invoice_amount < 10000 THEN '<10K'
        WHEN invoice_amount < 100000 THEN '10K-100K'
        WHEN invoice_amount < 1000000 THEN '100K-1M'
        ELSE '>1M'
    END as value_range,
    COUNT(*) as transaction_count,
    SUM(invoice_amount) as total_value
FROM trade_transactions
GROUP BY value_range;

-- Query 11: Flagged Entities
SELECT 
    COUNT(DISTINCT exporter_country_id) as flagged_exporters,
    COUNT(DISTINCT importer_country_id) as flagged_importers
FROM anomaly_results ar
JOIN trade_transactions t ON ar.transaction_id = t.transaction_id
WHERE ar.is_flagged = TRUE;

-- Query 12: Detection Accuracy
SELECT 
    SUM(CASE WHEN is_flagged THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as detection_rate,
    AVG(CASE WHEN anomaly_score > 0.5 THEN 1 ELSE 0 END) * 100.0 as accuracy_percentage
FROM anomaly_results;

-- Query 13: False Positive Rate
SELECT 
    COUNT(CASE WHEN is_flagged AND anomaly_score < 0.3 THEN 1 END) * 100.0 / COUNT(*) as false_positive_rate
FROM anomaly_results;

-- Query 14: Risk Score Distribution
SELECT 
    CASE 
        WHEN anomaly_score < 0.2 THEN 'MINIMAL'
        WHEN anomaly_score < 0.4 THEN 'LOW'
        WHEN anomaly_score < 0.6 THEN 'MEDIUM'
        WHEN anomaly_score < 0.8 THEN 'HIGH'
        ELSE 'CRITICAL'
    END as risk_category,
    COUNT(*) as count,
    AVG(anomaly_score) as avg_score
FROM anomaly_results
GROUP BY risk_category;
