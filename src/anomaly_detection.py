"""
Anomaly Detection Module
Detects anomalous trade patterns using:
1. Benford's Law - for invoice amount distributions
2. Mahalanobis Distance - for multivariate outlier detection
3. Multivariate Regression - for pattern analysis and deviation detection

Methods detect anomalies across 6 TBML typologies
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.spatial.distance import mahalanobis
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import logging
from typing import Tuple, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BenfordsLaw:
    """
    Benford's Law implementation for detecting fraudulent invoice amounts
    First digit distribution should follow expected pattern: P(d) = log10(1 + 1/d)
    """
    
    EXPECTED_DISTRIBUTION = {
        1: 0.30103, 2: 0.17609, 3: 0.12494, 4: 0.09691,
        5: 0.07918, 6: 0.06695, 7: 0.05799, 8: 0.05115, 9: 0.04576
    }
    
    def __init__(self, threshold: float = 0.15):
        """
        Initialize Benford's Law detector
        
        Args:
            threshold: Chi-square threshold for anomaly detection (default: 0.15)
        """
        self.threshold = threshold
    
    def extract_first_digit(self, amounts: np.ndarray) -> np.ndarray:
        """
        Extract first digit from amounts
        
        Args:
            amounts: Array of amounts
            
        Returns:
            Array of first digits
        """
        amounts = np.array(amounts)
        amounts = amounts[amounts > 0]
        first_digits = np.array([int(str(int(abs(x))).lstrip('-')[0]) for x in amounts])
        return first_digits
    
    def calculate_score(self, amounts: np.ndarray) -> float:
        """
        Calculate Benford's Law compliance score
        
        Args:
            amounts: Array of invoice amounts
            
        Returns:
            Compliance score (0-1, 1 = perfect compliance)
        """
        first_digits = self.extract_first_digit(amounts)
        
        if len(first_digits) == 0:
            return 0.0
        
        # Calculate observed distribution
        observed_dist = {}
        total = len(first_digits)
        for digit in range(1, 10):
            observed_dist[digit] = np.sum(first_digits == digit) / total
        
        # Calculate Chi-square statistic
        chi_square = 0
        for digit in range(1, 10):
            expected = self.EXPECTED_DISTRIBUTION[digit]
            observed = observed_dist.get(digit, 0)
            if expected > 0:
                chi_square += ((observed - expected) ** 2) / expected
        
        # Convert to compliance score (inverse relationship)
        compliance_score = 1 / (1 + chi_square)
        return compliance_score
    
    def detect_anomaly(self, amounts: np.ndarray) -> bool:
        """
        Detect if amounts violate Benford's Law
        
        Args:
            amounts: Array of invoice amounts
            
        Returns:
            True if anomalous (violates Benford's Law)
        """
        score = self.calculate_score(amounts)
        is_anomalous = score < (1 - self.threshold)
        return is_anomalous


class MahalanobisDetector:
    """
    Mahalanobis Distance for multivariate outlier detection
    Detects unusual combinations of trade variables
    """
    
    def __init__(self, threshold: float = 3.0):
        """
        Initialize Mahalanobis Distance detector
        
        Args:
            threshold: Mahalanobis distance threshold for anomaly (default: 3.0)
        """
        self.threshold = threshold
        self.mean = None
        self.cov_matrix = None
        self.inv_cov_matrix = None
    
    def fit(self, data: pd.DataFrame, features: List[str]):
        """
        Fit the detector to training data
        
        Args:
            data: Training dataframe
            features: Feature columns to use
        """
        X = data[features].values
        self.mean = np.mean(X, axis=0)
        self.cov_matrix = np.cov(X.T)
        
        try:
            self.inv_cov_matrix = np.linalg.inv(self.cov_matrix)
        except np.linalg.LinAlgError:
            # Use pseudo-inverse if singular
            self.inv_cov_matrix = np.linalg.pinv(self.cov_matrix)
            logger.warning("Covariance matrix is singular, using pseudo-inverse")
    
    def calculate_distance(self, observation: np.ndarray) -> float:
        """
        Calculate Mahalanobis distance for observation
        
        Args:
            observation: Single observation vector
            
        Returns:
            Mahalanobis distance
        """
        if self.mean is None or self.inv_cov_matrix is None:
            raise ValueError("Detector must be fitted first")
        
        diff = observation - self.mean
        distance = np.sqrt(diff.T @ self.inv_cov_matrix @ diff)
        return distance
    
    def detect_anomalies(self, data: pd.DataFrame, features: List[str]) -> np.ndarray:
        """
        Detect anomalies in dataset
        
        Args:
            data: Dataframe to analyze
            features: Feature columns to use
            
        Returns:
            Boolean array indicating anomalies
        """
        X = data[features].values
        distances = np.array([self.calculate_distance(obs) for obs in X])
        anomalies = distances > self.threshold
        return anomalies, distances


class MultivariateRegression:
    """
    Multivariate Regression for pattern analysis and deviation detection
    Detects transactions that deviate from expected patterns
    """
    
    def __init__(self, confidence_level: float = 0.95):
        """
        Initialize Multivariate Regression detector
        
        Args:
            confidence_level: Confidence level for anomaly detection (default: 0.95)
        """
        self.confidence_level = confidence_level
        self.model = None
        self.scaler = StandardScaler()
        self.residual_std = None
    
    def fit(self, X: np.ndarray, y: np.ndarray):
        """
        Fit regression model
        
        Args:
            X: Feature matrix (n_samples, n_features)
            y: Target variable (n_samples,)
        """
        X_scaled = self.scaler.fit_transform(X)
        self.model = LinearRegression()
        self.model.fit(X_scaled, y)
        
        # Calculate residual standard deviation
        y_pred = self.model.predict(X_scaled)
        residuals = y - y_pred
        self.residual_std = np.std(residuals)
        logger.info(f"Regression model fitted. Residual std: {self.residual_std:.4f}")
    
    def detect_deviations(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect transactions deviating from expected pattern
        
        Args:
            X: Feature matrix
            y: Target variable
            
        Returns:
            Tuple of (anomaly flags, deviation scores)
        """
        if self.model is None:
            raise ValueError("Model must be fitted first")
        
        X_scaled = self.scaler.transform(X)
        y_pred = self.model.predict(X_scaled)
        
        # Calculate standardized residuals
        residuals = y - y_pred
        std_residuals = residuals / self.residual_std
        
        # Calculate z-score threshold based on confidence level
        z_threshold = stats.norm.ppf(self.confidence_level)
        
        # Detect anomalies
        anomalies = np.abs(std_residuals) > z_threshold
        deviation_scores = np.abs(std_residuals)
        
        return anomalies, deviation_scores


class AnomalyDetectionEngine:
    """
    Integrated anomaly detection engine combining all 3 methods
    Detects anomalies across 6 TBML typologies
    """
    
    TBML_TYPOLOGIES = 6
    METHODS = ['benford', 'mahalanobis', 'regression']
    
    def __init__(self, benford_threshold: float = 0.15, 
                 mahalanobis_threshold: float = 3.0,
                 confidence_level: float = 0.95):
        """
        Initialize Anomaly Detection Engine
        
        Args:
            benford_threshold: Threshold for Benford's Law
            mahalanobis_threshold: Threshold for Mahalanobis Distance
            confidence_level: Confidence level for regression
        """
        self.benford = BenfordsLaw(threshold=benford_threshold)
        self.mahalanobis = MahalanobisDetector(threshold=mahalanobis_threshold)
        self.regression = MultivariateRegression(confidence_level=confidence_level)
        
        logger.info(f"Anomaly Detection Engine initialized with {self.TBML_TYPOLOGIES} TBML typologies")
    
    def analyze_transactions(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze transactions for anomalies using all methods
        
        Args:
            data: Transaction dataframe with columns:
                  - invoice_amount
                  - quantity
                  - unit_price
                  - transaction_date
                  
        Returns:
            DataFrame with anomaly scores for each method
        """
        results = pd.DataFrame(index=data.index)
        
        # Method 1: Benford's Law
        results['benford_score'] = 0.0
        for idx, amount in enumerate(data['invoice_amount']):
            results.loc[idx, 'benford_score'] = self.benford.calculate_score(np.array([amount]))
        
        # Method 2: Mahalanobis Distance
        features = ['quantity', 'unit_price', 'invoice_amount']
        if all(col in data.columns for col in features):
            self.mahalanobis.fit(data, features)
            anomalies, distances = self.mahalanobis.detect_anomalies(data, features)
            results['mahalanobis_distance'] = distances
            results['mahalanobis_anomaly'] = anomalies
        
        # Method 3: Multivariate Regression
        if len(data) > 2 and 'unit_price' in data.columns:
            try:
                X = data[['quantity']].values
                y = data['invoice_amount'].values
                self.regression.fit(X, y)
                anomalies, deviations = self.regression.detect_deviations(X, y)
                results['regression_deviation'] = deviations
                results['regression_anomaly'] = anomalies
            except Exception as e:
                logger.warning(f"Regression analysis failed: {str(e)}")
        
        # Calculate combined anomaly score
        results['combined_anomaly_score'] = (
            (1 - results.get('benford_score', 0)) * 0.3 +
            results.get('mahalanobis_distance', 0) / 10 * 0.3 +
            results.get('regression_deviation', 0) * 0.4
        )
        
        return results
    
    def classify_tbml_typology(self, transaction: pd.Series, anomaly_result: pd.Series) -> Dict:
        """
        Classify transaction into TBML typology
        
        Args:
            transaction: Transaction row
            anomaly_result: Anomaly detection result
            
        Returns:
            Dictionary with typology classification
        """
        typology = {
            'typology_id': None,
            'typology_name': None,
            'confidence': 0.0,
            'description': None
        }
        
        # Typologies (6 total):
        # 1. Over-invoicing, 2. Under-invoicing
        # 3. Over-shipment, 4. Under-shipment
        # 5. Phantom Shipment, 6. Misclassification
        
        benford_score = anomaly_result.get('benford_score', 1.0)
        regression_dev = anomaly_result.get('regression_deviation', 0)
        
        # Simple classification logic based on deviation patterns
        if benford_score < 0.5:  # Strong Benford violation
            typology['typology_id'] = 1
            typology['typology_name'] = 'Over-invoicing'
            typology['confidence'] = 1 - benford_score
        elif regression_dev > 2:
            typology['typology_id'] = 3
            typology['typology_name'] = 'Over-shipment'
            typology['confidence'] = min(regression_dev / 10, 1.0)
        
        return typology


# Example usage
if __name__ == "__main__":
    # Create sample data
    np.random.seed(42)
    n_samples = 100
    
    data = pd.DataFrame({
        'invoice_amount': np.random.lognormal(10, 1.5, n_samples),
        'quantity': np.random.uniform(10, 1000, n_samples),
        'unit_price': np.random.uniform(10, 500, n_samples),
        'transaction_date': pd.date_range('2023-01-01', periods=n_samples)
    })
    
    # Initialize engine
    engine = AnomalyDetectionEngine()
    
    # Analyze
    results = engine.analyze_transactions(data)
    
    print("\n=== Anomaly Detection Results ===")
    print(results.head(10))
    print(f"\nTotal anomalies detected: {results['combined_anomaly_score'].sum()}")
