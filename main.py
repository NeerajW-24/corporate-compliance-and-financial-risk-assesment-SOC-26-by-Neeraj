"""
Main Application Entry Point
Corporate Compliance and Financial Risk Assessment System

This orchestrates all components:
- 3 Dataset Integration (200+ economies)
- Anomaly Detection (Benford, Mahalanobis, Regression)
- TBML Detection (6 typologies)
- Power BI Dashboard (12+ KPIs)
"""

import sys
import os
import logging
import argparse
from datetime import datetime
import json

import pandas as pd
import numpy as np

from src.data_integration import DataIntegration
from src.anomaly_detection import AnomalyDetectionEngine
from src.tbml_detection import TBMLDetectionEngine
from src.dashboard.dashboard_config import DashboardConfiguration
from src.utils import load_configuration, categorize_risk, create_transaction_summary

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/main.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class ComplianceAnalyticsPipeline:
    """
    Main pipeline orchestrating all components
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the pipeline
        
        Args:
            config_path: Path to configuration file
        """
        self.config = load_configuration(config_path)
        self.integrated_data = None
        self.anomaly_results = None
        self.tbml_results = None
        
        logger.info("=" * 80)
        logger.info("Corporate Compliance and Financial Risk Assessment Pipeline")
        logger.info("Season of Code | WnCC, IIT Bombay [Mar'25]")
        logger.info("=" * 80)
    
    def stage1_data_integration(self):
        """
        Stage 1: Integrate 3 datasets covering 200+ economies
        
        Datasets:
        1. UN Comtrade Database
        2. World Bank Trade Statistics
        3. IMF Direction of Trade Statistics (DOTS)
        """
        logger.info("\n" + "=" * 80)
        logger.info("STAGE 1: DATA INTEGRATION (3 Datasets | 200+ Economies)")
        logger.info("=" * 80)
        
        try:
            db_connection = self.config.get('database', {})
            conn_string = f"postgresql://{db_connection.get('username')}:{db_connection.get('password')}@{db_connection.get('host')}:{db_connection.get('port')}/{db_connection.get('database')}"
            
            integrator = DataIntegration(conn_string)
            self.integrated_data = integrator.integrate_datasets()
            
            stats = integrator.get_economy_statistics()
            logger.info(f"✓ Data Integration Complete")
            logger.info(f"  - Total Transactions: {stats['total_transactions']}")
            logger.info(f"  - Exporters: {stats['exporters']}")
            logger.info(f"  - Importers: {stats['importers']}")
            logger.info(f"  - Total Trade Value: ${stats['total_value']:,.2f}")
            
            return True
            
        except Exception as e:
            logger.error(f"✗ Data Integration Failed: {str(e)}")
            return False
    
    def stage2_anomaly_detection(self):
        """
        Stage 2: Anomaly Detection using 3 methods
        
        Methods:
        1. Benford's Law - Invoice amount distribution
        2. Mahalanobis Distance - Multivariate outlier detection
        3. Multivariate Regression - Pattern analysis
        """
        logger.info("\n" + "=" * 80)
        logger.info("STAGE 2: ANOMALY DETECTION (3 Methods)")
        logger.info("=" * 80)
        
        if self.integrated_data is None:
            logger.error("✗ No integrated data available")
            return False
        
        try:
            engine = AnomalyDetectionEngine(
                benford_threshold=0.15,
                mahalanobis_threshold=3.0,
                confidence_level=0.95
            )
            
            # Sample for demonstration
            sample_data = self.integrated_data.head(100)
            self.anomaly_results = engine.analyze_transactions(sample_data)
            
            high_risk = (self.anomaly_results['combined_anomaly_score'] > 0.7).sum()
            
            logger.info(f"✓ Anomaly Detection Complete")
            logger.info(f"  - Benford's Law Score: Applied")
            logger.info(f"  - Mahalanobis Distance: Applied")
            logger.info(f"  - Multivariate Regression: Applied")
            logger.info(f"  - High Risk Transactions: {high_risk}")
            
            return True
            
        except Exception as e:
            logger.error(f"✗ Anomaly Detection Failed: {str(e)}")
            return False
    
    def stage3_tbml_detection(self):
        """
        Stage 3: TBML Detection - 6 Typologies
        
        Typologies:
        1. Over-invoicing
        2. Under-invoicing
        3. Over-shipment
        4. Under-shipment
        5. Phantom Shipment
        6. Misclassification
        """
        logger.info("\n" + "=" * 80)
        logger.info("STAGE 3: TBML DETECTION (6 Typologies)")
        logger.info("=" * 80)
        
        if self.integrated_data is None:
            logger.error("✗ No integrated data available")
            return False
        
        try:
            engine = TBMLDetectionEngine()
            
            # Sample for demonstration
            sample_data = self.integrated_data.head(100)
            self.tbml_results = engine.generate_tbml_report(sample_data)
            
            logger.info(f"✓ TBML Detection Complete")
            logger.info(f"  - Total Transactions Analyzed: {self.tbml_results['total_transactions']}")
            
            for typology, stats in self.tbml_results['typology_statistics'].items():
                if stats['detected_count'] > 0:
                    logger.info(f"  - {typology}: {stats['detected_count']} detected "
                              f"(Confidence: {stats['average_confidence']:.2%})")
            
            logger.info(f"  - Overall Detection Rate: {self.tbml_results['summary']['detection_rate']:.2f}%")
            
            return True
            
        except Exception as e:
            logger.error(f"✗ TBML Detection Failed: {str(e)}")
            return False
    
    def stage4_dashboard_configuration(self):
        """
        Stage 4: Dashboard Configuration
        
        12+ Compliance KPIs:
        1. Total Transactions Monitored
        2. Anomalies Detected (All Methods)
        3. High Risk Transactions
        4. Average Mahalanobis Distance
        5. Benford's Law Compliance %
        6. Multivariate Regression Deviations
        7. TBML Typology Distribution
        8. Economy-wise Risk Heatmap
        9. Temporal Trend Analysis
        10. Transaction Value Distribution
        11. Flagged Entities
        12. Detection Accuracy
        ... and more
        """
        logger.info("\n" + "=" * 80)
        logger.info("STAGE 4: POWER BI DASHBOARD (12+ KPIs)")
        logger.info("=" * 80)
        
        try:
            dashboard = DashboardConfiguration()
            
            logger.info(f"✓ Dashboard Configuration Complete")
            logger.info(f"  - Platform: Power BI")
            logger.info(f"  - Total KPIs: {len(DashboardConfiguration.KPIS)}")
            logger.info(f"  - Dashboard Pages: 5")
            
            for kpi in DashboardConfiguration.KPIS:
                logger.info(f"    • {kpi.kpi_id}. {kpi.name}")
            
            return True
            
        except Exception as e:
            logger.error(f"✗ Dashboard Configuration Failed: {str(e)}")
            return False
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        logger.info("\n" + "=" * 80)
        logger.info("SUMMARY REPORT")
        logger.info("=" * 80)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'project': 'Corporate Compliance and Financial Risk Assessment',
            'event': 'Season of Code | WnCC, IIT Bombay [Mar\'25]',
            'components': {
                'datasets_integrated': 3,
                'economies_covered': 200,
                'anomaly_detection_methods': 3,
                'tbml_typologies': 6,
                'dashboard_kpis': len(DashboardConfiguration.KPIS)
            }
        }
        
        if self.integrated_data is not None:
            report['data_summary'] = create_transaction_summary(self.integrated_data)
        
        if self.anomaly_results is not None:
            report['anomaly_summary'] = {
                'total_anomalies': len(self.anomaly_results[self.anomaly_results['combined_anomaly_score'] > 0.5]),
                'high_risk_count': len(self.anomaly_results[self.anomaly_results['combined_anomaly_score'] > 0.7])
            }
        
        if self.tbml_results is not None:
            report['tbml_summary'] = self.tbml_results['summary']
        
        logger.info(json.dumps(report, indent=2, default=str))
        
        return report
    
    def run_full_pipeline(self):
        """Run the complete pipeline"""
        logger.info("\nStarting Full Pipeline Execution...\n")
        
        stages = [
            ("Data Integration", self.stage1_data_integration),
            ("Anomaly Detection", self.stage2_anomaly_detection),
            ("TBML Detection", self.stage3_tbml_detection),
            ("Dashboard Configuration", self.stage4_dashboard_configuration)
        ]
        
        results = {}
        for stage_name, stage_func in stages:
            results[stage_name] = stage_func()
        
        # Generate final report
        self.generate_summary_report()
        
        logger.info("\n" + "=" * 80)
        logger.info("PIPELINE EXECUTION COMPLETE")
        logger.info("=" * 80 + "\n")
        
        return results


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Corporate Compliance and Financial Risk Assessment System'
    )
    parser.add_argument('--config', type=str, default='config/config.yaml',
                       help='Configuration file path')
    parser.add_argument('--stage', type=str, choices=['1', '2', '3', '4', 'all'],
                       default='all', help='Pipeline stage to run')
    
    args = parser.parse_args()
    
    pipeline = ComplianceAnalyticsPipeline(args.config)
    
    if args.stage == 'all':
        pipeline.run_full_pipeline()
    else:
        stage_map = {
            '1': pipeline.stage1_data_integration,
            '2': pipeline.stage2_anomaly_detection,
            '3': pipeline.stage3_tbml_detection,
            '4': pipeline.stage4_dashboard_configuration
        }
        stage_map[args.stage]()


if __name__ == "__main__":
    main()
