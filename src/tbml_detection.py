"""
TBML Detection Module
Trade-Based Money Laundering (TBML) Detection System

Detects 6 TBML typologies:
1. Over-invoicing: Goods invoiced above market prices
2. Under-invoicing: Goods invoiced below market prices
3. Over-shipment: Actual goods exceed documented quantity
4. Under-shipment: Actual goods less than documented quantity
5. Phantom Shipment: No actual goods, only documentation
6. Misclassification: Goods classified under wrong HS codes
"""

import numpy as np
import pandas as pd
from enum import Enum
from typing import Dict, List, Tuple
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TBMLTypology(Enum):
    """Enum for 6 TBML Typologies"""
    OVER_INVOICING = 1
    UNDER_INVOICING = 2
    OVER_SHIPMENT = 3
    UNDER_SHIPMENT = 4
    PHANTOM_SHIPMENT = 5
    MISCLASSIFICATION = 6


class TBMLDetectionEngine:
    """
    Comprehensive TBML Detection Engine for 6 typologies
    """
    
    TYPOLOGIES_COUNT = 6
    
    # Risk profiles for each typology
    TYPOLOGY_PROFILES = {
        TBMLTypology.OVER_INVOICING: {
            'description': 'Exporters invoice goods at significantly higher prices than market',
            'risk_level': 'high',
            'typical_price_deviation': (1.3, 3.0),  # 30-200% above market
            'typical_goods': ['Diamonds', 'Precious Metals', 'Electronics'],
            'detection_features': ['unit_price', 'invoice_amount', 'market_price']
        },
        TBMLTypology.UNDER_INVOICING: {
            'description': 'Exporters invoice goods at significantly lower prices than market',
            'risk_level': 'high',
            'typical_price_deviation': (0.1, 0.7),  # 10-70% of market price
            'typical_goods': ['Commodities', 'Raw Materials', 'Textiles'],
            'detection_features': ['unit_price', 'invoice_amount', 'market_price']
        },
        TBMLTypology.OVER_SHIPMENT: {
            'description': 'Actual goods shipped exceed quantity in commercial documents',
            'risk_level': 'high',
            'typical_quantity_deviation': (1.2, 5.0),  # 20-400% more
            'typical_goods': ['Minerals', 'Oil', 'Agricultural Products'],
            'detection_features': ['quantity', 'documented_quantity', 'weight', 'volume']
        },
        TBMLTypology.UNDER_SHIPMENT: {
            'description': 'Actual goods shipped less than quantity in commercial documents',
            'risk_level': 'medium',
            'typical_quantity_deviation': (0.5, 0.8),  # 50-80% of documented
            'typical_goods': ['High-value goods', 'Components'],
            'detection_features': ['quantity', 'documented_quantity', 'weight']
        },
        TBMLTypology.PHANTOM_SHIPMENT: {
            'description': 'No actual goods shipment, only documentation transfer',
            'risk_level': 'critical',
            'indicators': ['no_physical_movement', 'repeated_documentation', 'circular_flow'],
            'typical_goods': ['Any commodity'],
            'detection_features': ['shipping_records', 'port_data', 'document_patterns']
        },
        TBMLTypology.MISCLASSIFICATION: {
            'description': 'Goods classified under incorrect HS codes to manipulate duties/restrictions',
            'risk_level': 'high',
            'typical_hs_deviation': 'adjacent_hs_codes',
            'typical_goods': ['Sensitive goods', 'Restricted items'],
            'detection_features': ['hs_code', 'description', 'unit_price', 'properties']
        }
    }
    
    def __init__(self, market_price_db: Dict = None):
        """
        Initialize TBML Detection Engine
        
        Args:
            market_price_db: Dictionary of reference market prices by commodity
        """
        self.market_price_db = market_price_db or {}
        self.typologies = list(TBMLTypology)
        logger.info(f"TBML Detection Engine initialized with {self.TYPOLOGIES_COUNT} typologies")
    
    def detect_over_invoicing(self, transaction: pd.Series, market_price: float = None) -> Dict:
        """
        Detect Over-Invoicing typology (Type 1)
        
        Args:
            transaction: Transaction data
            market_price: Reference market price
            
        Returns:
            Detection result dictionary
        """
        result = {
            'typology': TBMLTypology.OVER_INVOICING,
            'detected': False,
            'confidence': 0.0,
            'deviation_ratio': 0.0,
            'details': {}
        }
        
        if market_price is None or market_price == 0:
            return result
        
        unit_price = transaction.get('unit_price', 0)
        invoice_amount = transaction.get('invoice_amount', 0)
        quantity = transaction.get('quantity', 1)
        
        if quantity == 0:
            return result
        
        # Calculate deviation ratio
        calculated_price = invoice_amount / quantity
        deviation_ratio = calculated_price / market_price
        
        result['deviation_ratio'] = deviation_ratio
        result['details'] = {
            'market_price': market_price,
            'invoice_price': calculated_price,
            'quantity': quantity,
            'total_amount': invoice_amount
        }
        
        # Detect over-invoicing (price deviation > 1.3x market price)
        if deviation_ratio > 1.3:
            result['detected'] = True
            result['confidence'] = min((deviation_ratio - 1.0) / 2.0, 1.0)
        
        return result
    
    def detect_under_invoicing(self, transaction: pd.Series, market_price: float = None) -> Dict:
        """
        Detect Under-Invoicing typology (Type 2)
        
        Args:
            transaction: Transaction data
            market_price: Reference market price
            
        Returns:
            Detection result dictionary
        """
        result = {
            'typology': TBMLTypology.UNDER_INVOICING,
            'detected': False,
            'confidence': 0.0,
            'deviation_ratio': 0.0,
            'details': {}
        }
        
        if market_price is None or market_price == 0:
            return result
        
        unit_price = transaction.get('unit_price', 0)
        invoice_amount = transaction.get('invoice_amount', 0)
        quantity = transaction.get('quantity', 1)
        
        if quantity == 0:
            return result
        
        # Calculate deviation ratio
        calculated_price = invoice_amount / quantity
        deviation_ratio = calculated_price / market_price
        
        result['deviation_ratio'] = deviation_ratio
        result['details'] = {
            'market_price': market_price,
            'invoice_price': calculated_price,
            'quantity': quantity,
            'total_amount': invoice_amount
        }
        
        # Detect under-invoicing (price deviation < 0.7x market price)
        if deviation_ratio < 0.7:
            result['detected'] = True
            result['confidence'] = min((1.0 - deviation_ratio), 1.0)
        
        return result
    
    def detect_over_shipment(self, transaction: pd.Series, 
                           documented_quantity: float = None) -> Dict:
        """
        Detect Over-Shipment typology (Type 3)
        
        Args:
            transaction: Transaction data
            documented_quantity: Quantity documented in commercial papers
            
        Returns:
            Detection result dictionary
        """
        result = {
            'typology': TBMLTypology.OVER_SHIPMENT,
            'detected': False,
            'confidence': 0.0,
            'quantity_ratio': 0.0,
            'details': {}
        }
        
        if documented_quantity is None or documented_quantity == 0:
            return result
        
        actual_quantity = transaction.get('quantity', 0)
        
        # Calculate quantity ratio
        quantity_ratio = actual_quantity / documented_quantity
        
        result['quantity_ratio'] = quantity_ratio
        result['details'] = {
            'actual_quantity': actual_quantity,
            'documented_quantity': documented_quantity,
            'excess_quantity': actual_quantity - documented_quantity,
            'excess_percentage': ((actual_quantity - documented_quantity) / documented_quantity) * 100
        }
        
        # Detect over-shipment (quantity ratio > 1.2)
        if quantity_ratio > 1.2:
            result['detected'] = True
            result['confidence'] = min((quantity_ratio - 1.0) / 4.0, 1.0)
        
        return result
    
    def detect_under_shipment(self, transaction: pd.Series, 
                            documented_quantity: float = None) -> Dict:
        """
        Detect Under-Shipment typology (Type 4)
        
        Args:
            transaction: Transaction data
            documented_quantity: Quantity documented in commercial papers
            
        Returns:
            Detection result dictionary
        """
        result = {
            'typology': TBMLTypology.UNDER_SHIPMENT,
            'detected': False,
            'confidence': 0.0,
            'quantity_ratio': 0.0,
            'details': {}
        }
        
        if documented_quantity is None or documented_quantity == 0:
            return result
        
        actual_quantity = transaction.get('quantity', 0)
        
        # Calculate quantity ratio
        quantity_ratio = actual_quantity / documented_quantity
        
        result['quantity_ratio'] = quantity_ratio
        result['details'] = {
            'actual_quantity': actual_quantity,
            'documented_quantity': documented_quantity,
            'missing_quantity': documented_quantity - actual_quantity,
            'missing_percentage': ((documented_quantity - actual_quantity) / documented_quantity) * 100
        }
        
        # Detect under-shipment (quantity ratio < 0.8)
        if quantity_ratio < 0.8:
            result['detected'] = True
            result['confidence'] = min(1.0 - quantity_ratio, 1.0)
        
        return result
    
    def detect_phantom_shipment(self, transaction: pd.Series,
                               shipping_records: List[Dict] = None) -> Dict:
        """
        Detect Phantom Shipment typology (Type 5)
        
        Args:
            transaction: Transaction data
            shipping_records: Actual shipping/port records
            
        Returns:
            Detection result dictionary
        """
        result = {
            'typology': TBMLTypology.PHANTOM_SHIPMENT,
            'detected': False,
            'confidence': 0.0,
            'physical_evidence_score': 0.0,
            'details': {}
        }
        
        if shipping_records is None:
            shipping_records = []
        
        transaction_id = transaction.get('transaction_id')
        transaction_date = transaction.get('transaction_date')
        
        # Check for physical shipping evidence
        matching_shipments = len([s for s in shipping_records 
                                if s.get('transaction_id') == transaction_id])
        
        physical_evidence_score = matching_shipments / max(len(shipping_records), 1)
        
        result['physical_evidence_score'] = physical_evidence_score
        result['details'] = {
            'documented_transaction': True,
            'physical_shipment_found': matching_shipments > 0,
            'shipping_records_count': matching_shipments,
            'transaction_id': transaction_id
        }
        
        # Detect phantom shipment (no physical evidence)
        if matching_shipments == 0 and len(shipping_records) > 0:
            result['detected'] = True
            result['confidence'] = 0.9
        
        return result
    
    def detect_misclassification(self, transaction: pd.Series,
                                correct_hs_code: str = None) -> Dict:
        """
        Detect Misclassification typology (Type 6)
        
        Args:
            transaction: Transaction data
            correct_hs_code: Correct HS code for the commodity
            
        Returns:
            Detection result dictionary
        """
        result = {
            'typology': TBMLTypology.MISCLASSIFICATION,
            'detected': False,
            'confidence': 0.0,
            'code_deviation': 0.0,
            'details': {}
        }
        
        if correct_hs_code is None:
            return result
        
        reported_hs_code = transaction.get('hs_code', '')
        
        # Calculate code similarity (simplified: check if codes are adjacent)
        if reported_hs_code == correct_hs_code:
            return result
        
        # Convert to integers for comparison
        try:
            reported_code_int = int(reported_hs_code[:4])  # First 4 digits
            correct_code_int = int(correct_hs_code[:4])
            
            code_deviation = abs(reported_code_int - correct_code_int)
            
            result['code_deviation'] = code_deviation
            result['details'] = {
                'reported_hs_code': reported_hs_code,
                'correct_hs_code': correct_hs_code,
                'code_difference': code_deviation,
                'description': transaction.get('description', '')
            }
            
            # Detect misclassification (codes differ by adjacent classification)
            if code_deviation > 0 and code_deviation <= 100:
                result['detected'] = True
                result['confidence'] = min(1.0 / (1.0 + code_deviation), 0.9)
        
        except (ValueError, TypeError):
            pass
        
        return result
    
    def analyze_transaction(self, transaction: pd.Series, 
                          market_price: float = None,
                          documented_quantity: float = None,
                          shipping_records: List[Dict] = None,
                          correct_hs_code: str = None) -> List[Dict]:
        """
        Analyze transaction for all 6 TBML typologies
        
        Args:
            transaction: Transaction data
            market_price: Reference market price
            documented_quantity: Documented quantity
            shipping_records: Shipping records for phantom detection
            correct_hs_code: Correct HS code
            
        Returns:
            List of detection results for all typologies
        """
        results = [
            self.detect_over_invoicing(transaction, market_price),
            self.detect_under_invoicing(transaction, market_price),
            self.detect_over_shipment(transaction, documented_quantity),
            self.detect_under_shipment(transaction, documented_quantity),
            self.detect_phantom_shipment(transaction, shipping_records),
            self.detect_misclassification(transaction, correct_hs_code)
        ]
        
        return results
    
    def generate_tbml_report(self, transactions: pd.DataFrame) -> Dict:
        """
        Generate comprehensive TBML detection report
        
        Args:
            transactions: DataFrame of transactions
            
        Returns:
            Dictionary with detection statistics
        """
        report = {
            'total_transactions': len(transactions),
            'detection_timestamp': datetime.now().isoformat(),
            'typology_statistics': {},
            'high_risk_transactions': [],
            'summary': {}
        }
        
        # Initialize typology stats
        for typology in TBMLTypology:
            report['typology_statistics'][typology.name] = {
                'detected_count': 0,
                'average_confidence': 0.0,
                'risk_level': self.TYPOLOGY_PROFILES[typology]['risk_level']
            }
        
        # Analyze all transactions
        detections_per_typology = {t: [] for t in TBMLTypology}
        
        for idx, transaction in transactions.iterrows():
            detections = self.analyze_transaction(transaction)
            
            for detection in detections:
                typology = detection['typology']
                if detection['detected']:
                    detections_per_typology[typology].append(detection['confidence'])
                    report['typology_statistics'][typology.name]['detected_count'] += 1
        
        # Calculate average confidence for each typology
        for typology in TBMLTypology:
            confidences = detections_per_typology[typology]
            if confidences:
                report['typology_statistics'][typology.name]['average_confidence'] = \
                    sum(confidences) / len(confidences)
        
        # Summary
        total_detections = sum(stats['detected_count'] 
                              for stats in report['typology_statistics'].values())
        
        report['summary'] = {
            'total_detections': total_detections,
            'detection_rate': (total_detections / len(transactions)) * 100 if len(transactions) > 0 else 0,
            'most_common_typology': max(report['typology_statistics'].items(),
                                       key=lambda x: x[1]['detected_count'])[0]
        }
        
        return report


# Example usage
if __name__ == "__main__":
    # Create sample transaction
    sample_transaction = pd.Series({
        'transaction_id': 'T001',
        'invoice_amount': 150000,
        'quantity': 100,
        'unit_price': 1500,
        'hs_code': '440799',
        'description': 'Wood products'
    })
    
    # Initialize engine
    engine = TBMLDetectionEngine()
    
    # Analyze transaction
    detections = engine.analyze_transaction(
        sample_transaction,
        market_price=1000,
        documented_quantity=80,
        correct_hs_code='440710'
    )
    
    print("\n=== TBML Typologies Detection (6 Total) ===")
    for i, detection in enumerate(detections, 1):
        if detection['detected']:
            print(f"✓ Typology {i}: {detection['typology'].name}")
            print(f"  Confidence: {detection['confidence']:.2%}")
