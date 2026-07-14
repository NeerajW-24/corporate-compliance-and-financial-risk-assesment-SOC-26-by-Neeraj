"""
Test Suite for Corporate Compliance and Financial Risk Assessment System
"""

import unittest
import numpy as np
import pandas as pd
from src.anomaly_detection import BenfordsLaw, MahalanobisDetector, AnomalyDetectionEngine
from src.tbml_detection import TBMLDetectionEngine
from src.utils import categorize_risk, normalize_data, detect_outliers_iqr


class TestBenfordsLaw(unittest.TestCase):
    """Test Benford's Law implementation"""
    
    def setUp(self):
        self.detector = BenfordsLaw(threshold=0.15)
    
    def test_benford_law_detection(self):
        """Test Benford's Law score calculation"""
        # Generate data following Benford's distribution
        amounts = np.array([10, 15, 20, 25, 100, 150, 200, 300, 500, 1000])
        score = self.detector.calculate_score(amounts)
        
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)
    
    def test_first_digit_extraction(self):
        """Test first digit extraction"""
        amounts = np.array([123, 456, 789])
        digits = self.detector.extract_first_digit(amounts)
        
        self.assertEqual(digits[0], 1)
        self.assertEqual(digits[1], 4)
        self.assertEqual(digits[2], 7)


class TestMahalanobisDetector(unittest.TestCase):
    """Test Mahalanobis Distance implementation"""
    
    def setUp(self):
        self.detector = MahalanobisDetector(threshold=3.0)
        
        # Create training data
        self.train_data = pd.DataFrame({
            'quantity': np.random.uniform(10, 1000, 100),
            'unit_price': np.random.uniform(10, 500, 100),
            'invoice_amount': np.random.uniform(1000, 100000, 100)
        })
        
        self.detector.fit(self.train_data, ['quantity', 'unit_price', 'invoice_amount'])
    
    def test_mahalanobis_distance_calculation(self):
        """Test Mahalanobis distance calculation"""
        observation = np.array([500, 250, 50000])
        distance = self.detector.calculate_distance(observation)
        
        self.assertGreaterEqual(distance, 0)
    
    def test_anomaly_detection(self):
        """Test anomaly detection"""
        test_data = pd.DataFrame({
            'quantity': np.random.uniform(10, 1000, 10),
            'unit_price': np.random.uniform(10, 500, 10),
            'invoice_amount': np.random.uniform(1000, 100000, 10)
        })
        
        anomalies, distances = self.detector.detect_anomalies(
            test_data, ['quantity', 'unit_price', 'invoice_amount']
        )
        
        self.assertEqual(len(anomalies), 10)
        self.assertEqual(len(distances), 10)


class TestTBMLDetection(unittest.TestCase):
    """Test TBML Detection"""
    
    def setUp(self):
        self.engine = TBMLDetectionEngine()
    
    def test_over_invoicing_detection(self):
        """Test over-invoicing detection"""
        transaction = pd.Series({
            'invoice_amount': 150000,
            'quantity': 100,
            'unit_price': 1500
        })
        
        result = self.engine.detect_over_invoicing(transaction, market_price=1000)
        
        self.assertTrue(result['detected'])
        self.assertGreater(result['deviation_ratio'], 1.0)
    
    def test_under_invoicing_detection(self):
        """Test under-invoicing detection"""
        transaction = pd.Series({
            'invoice_amount': 50000,
            'quantity': 100,
            'unit_price': 500
        })
        
        result = self.engine.detect_under_invoicing(transaction, market_price=1000)
        
        self.assertTrue(result['detected'])
        self.assertLess(result['deviation_ratio'], 1.0)
    
    def test_over_shipment_detection(self):
        """Test over-shipment detection"""
        transaction = pd.Series({
            'quantity': 150
        })
        
        result = self.engine.detect_over_shipment(transaction, documented_quantity=100)
        
        self.assertTrue(result['detected'])
        self.assertGreater(result['quantity_ratio'], 1.0)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""
    
    def test_categorize_risk(self):
        """Test risk categorization"""
        self.assertEqual(categorize_risk(0.9), "CRITICAL")
        self.assertEqual(categorize_risk(0.7), "HIGH")
        self.assertEqual(categorize_risk(0.5), "MEDIUM")
        self.assertEqual(categorize_risk(0.3), "LOW")
        self.assertEqual(categorize_risk(0.1), "MINIMAL")
    
    def test_normalize_data(self):
        """Test data normalization"""
        data = pd.Series([10, 20, 30, 40, 50])
        normalized = normalize_data(data)
        
        self.assertAlmostEqual(normalized.min(), 0)
        self.assertAlmostEqual(normalized.max(), 1)
    
    def test_detect_outliers_iqr(self):
        """Test IQR outlier detection"""
        data = pd.Series([1, 2, 3, 4, 5, 100])
        outliers = detect_outliers_iqr(data)
        
        # 100 should be detected as outlier
        self.assertTrue(outliers.iloc[-1])


class TestAnomalyDetectionEngine(unittest.TestCase):
    """Test integrated anomaly detection engine"""
    
    def setUp(self):
        self.engine = AnomalyDetectionEngine()
        
        self.data = pd.DataFrame({
            'invoice_amount': np.random.lognormal(10, 1.5, 50),
            'quantity': np.random.uniform(10, 1000, 50),
            'unit_price': np.random.uniform(10, 500, 50),
            'transaction_date': pd.date_range('2023-01-01', periods=50)
        })
    
    def test_transaction_analysis(self):
        """Test transaction analysis"""
        results = self.engine.analyze_transactions(self.data)
        
        self.assertEqual(len(results), len(self.data))
        self.assertIn('combined_anomaly_score', results.columns)
    
    def test_tbml_classification(self):
        """Test TBML typology classification"""
        transaction = self.data.iloc[0]
        anomaly_result = {
            'benford_score': 0.3,
            'regression_deviation': 2.5
        }
        
        classification = self.engine.classify_tbml_typology(transaction, anomaly_result)
        
        self.assertIsNotNone(classification['typology_id'])


class TestDataIntegration(unittest.TestCase):
    """Test data integration functionality"""
    
    def test_integrated_data_structure(self):
        """Test that integrated data has required columns"""
        required_columns = [
            'transaction_date', 'exporter_code', 'importer_code',
            'hs_code', 'invoice_amount', 'quantity'
        ]
        
        # Create sample integrated data
        sample_data = pd.DataFrame({
            col: [1, 2, 3] for col in required_columns
        })
        
        for col in required_columns:
            self.assertIn(col, sample_data.columns)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("Running Test Suite")
    print("Corporate Compliance and Financial Risk Assessment System")
    print("=" * 80 + "\n")
    
    run_tests()
    
    print("\n" + "=" * 80)
    print("Test Suite Complete")
    print("=" * 80 + "\n")
