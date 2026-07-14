"""
Utility Functions and Helpers
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging
from typing import Dict, List, Tuple, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_configuration(config_path: str) -> Dict:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config.yaml
        
    Returns:
        Configuration dictionary
    """
    import yaml
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        return {}


def generate_report_timestamp() -> str:
    """Generate timestamp for reports"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format value as percentage"""
    return f"{value * 100:.{decimals}f}%"


def format_currency(value: float, currency: str = "USD") -> str:
    """Format value as currency"""
    if currency == "USD":
        return f"${value:,.2f}"
    return f"{value:,.2f} {currency}"


def calculate_statistics(data: pd.Series) -> Dict:
    """
    Calculate statistical measures
    
    Args:
        data: Pandas series
        
    Returns:
        Dictionary with statistics
    """
    return {
        'count': len(data),
        'mean': float(data.mean()),
        'median': float(data.median()),
        'std': float(data.std()),
        'min': float(data.min()),
        'max': float(data.max()),
        'q25': float(data.quantile(0.25)),
        'q75': float(data.quantile(0.75)),
    }


def detect_outliers_iqr(data: pd.Series, multiplier: float = 1.5) -> np.ndarray:
    """
    Detect outliers using IQR method
    
    Args:
        data: Pandas series
        multiplier: IQR multiplier (default 1.5)
        
    Returns:
        Boolean array indicating outliers
    """
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    return (data < lower_bound) | (data > upper_bound)


def normalize_data(data: pd.Series) -> pd.Series:
    """
    Normalize data to 0-1 range
    
    Args:
        data: Pandas series
        
    Returns:
        Normalized series
    """
    min_val = data.min()
    max_val = data.max()
    
    if max_val == min_val:
        return pd.Series(np.zeros(len(data)), index=data.index)
    
    return (data - min_val) / (max_val - min_val)


def categorize_risk(score: float) -> str:
    """
    Categorize risk based on score
    
    Args:
        score: Risk score (0-1)
        
    Returns:
        Risk category
    """
    if score >= 0.8:
        return "CRITICAL"
    elif score >= 0.6:
        return "HIGH"
    elif score >= 0.4:
        return "MEDIUM"
    elif score >= 0.2:
        return "LOW"
    else:
        return "MINIMAL"


def validate_transaction_data(transaction: Dict) -> Tuple[bool, List[str]]:
    """
    Validate transaction data completeness
    
    Args:
        transaction: Transaction dictionary
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    required_fields = [
        'transaction_id', 'transaction_date', 'exporter_code',
        'importer_code', 'hs_code', 'invoice_amount', 'quantity'
    ]
    
    errors = []
    
    for field in required_fields:
        if field not in transaction or transaction[field] is None:
            errors.append(f"Missing required field: {field}")
    
    # Validate numeric fields
    if 'invoice_amount' in transaction:
        try:
            if float(transaction['invoice_amount']) < 0:
                errors.append("invoice_amount must be positive")
        except (ValueError, TypeError):
            errors.append("invoice_amount must be numeric")
    
    if 'quantity' in transaction:
        try:
            if float(transaction['quantity']) < 0:
                errors.append("quantity must be positive")
        except (ValueError, TypeError):
            errors.append("quantity must be numeric")
    
    return len(errors) == 0, errors


def export_dataframe_to_excel(df: pd.DataFrame, filepath: str, 
                             sheet_name: str = "Data"):
    """
    Export DataFrame to Excel file
    
    Args:
        df: Pandas DataFrame
        filepath: Output file path
        sheet_name: Sheet name in Excel
    """
    try:
        df.to_excel(filepath, sheet_name=sheet_name, index=False)
        logger.info(f"Data exported to {filepath}")
    except Exception as e:
        logger.error(f"Error exporting to Excel: {str(e)}")


def export_dataframe_to_csv(df: pd.DataFrame, filepath: str):
    """
    Export DataFrame to CSV file
    
    Args:
        df: Pandas DataFrame
        filepath: Output file path
    """
    try:
        df.to_csv(filepath, index=False)
        logger.info(f"Data exported to {filepath}")
    except Exception as e:
        logger.error(f"Error exporting to CSV: {str(e)}")


def create_transaction_summary(transactions: pd.DataFrame) -> Dict:
    """
    Create summary statistics for transaction dataset
    
    Args:
        transactions: DataFrame of transactions
        
    Returns:
        Summary dictionary
    """
    summary = {
        'total_transactions': len(transactions),
        'unique_exporters': transactions['exporter_code'].nunique(),
        'unique_importers': transactions['importer_code'].nunique(),
        'unique_commodities': transactions.get('hs_code', pd.Series()).nunique(),
        'total_value': float(transactions.get('invoice_amount', pd.Series()).sum()),
        'average_value': float(transactions.get('invoice_amount', pd.Series()).mean()),
        'date_range': {
            'start': str(transactions['transaction_date'].min()),
            'end': str(transactions['transaction_date'].max())
        }
    }
    
    return summary


# Example usage
if __name__ == "__main__":
    # Create sample data
    sample_data = pd.Series([100, 150, 200, 250, 1000])
    
    print("\n=== Utility Functions Demo ===")
    print(f"Statistics: {calculate_statistics(sample_data)}")
    print(f"Outliers (IQR): {detect_outliers_iqr(sample_data).tolist()}")
    print(f"Risk Category (0.75): {categorize_risk(0.75)}")
    print(f"Formatted Currency: {format_currency(12345.67)}")
    print(f"Formatted Percentage: {format_percentage(0.8567)}")
