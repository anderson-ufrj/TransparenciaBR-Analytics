"""
Data processing module for cleaning, transforming, and preparing data for analysis.
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Callable
import pandas as pd
import numpy as np
from datetime import datetime
import re


class DataProcessor:
    """
    Data processor for cleaning and transforming Portal da Transparência data.
    
    Features:
    - Data type standardization
    - Missing value handling
    - Date parsing and normalization
    - Currency value cleaning
    - Feature engineering
    - Data validation
    """
    
    def __init__(self, input_dir: str = "data/raw", output_dir: str = "data/processed"):
        """
        Initialize data processor.
        
        Args:
            input_dir: Directory containing raw data
            output_dir: Directory to save processed data
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Define processing configurations
        self.processing_configs = self._get_processing_configs()
    
    def _get_processing_configs(self) -> Dict[str, Dict[str, Any]]:
        """Get processing configuration for each data type."""
        return {
            "contratos": {
                "date_columns": ["dataAssinatura", "dataInicioVigencia", "dataFimVigencia"],
                "value_columns": ["valorInicial", "valorFinal"],
                "id_columns": ["numero", "codigoContrato"],
                "text_columns": ["objeto", "modalidadeCompra", "situacao"]
            },
            "pagamentos": {
                "date_columns": ["data", "dataDocumento"],
                "value_columns": ["valor", "valorDocumento"],
                "id_columns": ["codigoFavorecido", "numeroDocumento"],
                "text_columns": ["nomeFavorecido", "observacao"]
            },
            "licitacoes": {
                "date_columns": ["dataAbertura", "dataResultado", "dataPublicacao"],
                "value_columns": ["valorEstimado", "valorHomologado"],
                "id_columns": ["numero", "codigoUG"],
                "text_columns": ["objeto", "modalidade", "situacao"]
            },
            "fornecedores": {
                "date_columns": ["dataCredenciamento"],
                "value_columns": [],
                "id_columns": ["id", "cnpjCpf"],
                "text_columns": ["nome", "nomeFantasia", "municipio", "uf"]
            },
            "orgaos": {
                "date_columns": [],
                "value_columns": [],
                "id_columns": ["codigo", "codigoSiafi"],
                "text_columns": ["nome", "sigla", "descricao"]
            }
        }
    
    def process_dataset(
        self,
        dataset_name: str,
        input_file: Optional[Union[str, Path]] = None,
        custom_processing: Optional[Callable] = None
    ) -> pd.DataFrame:
        """
        Process a specific dataset.
        
        Args:
            dataset_name: Name of the dataset to process
            input_file: Specific input file (optional, uses latest if not provided)
            custom_processing: Custom processing function to apply
            
        Returns:
            Processed DataFrame
        """
        self.logger.info(f"Processing dataset: {dataset_name}")
        
        # Load data
        if input_file:
            df = pd.read_parquet(input_file)
        else:
            df = self._load_latest_data(dataset_name)
        
        if df is None or df.empty:
            self.logger.warning(f"No data found for {dataset_name}")
            return pd.DataFrame()
        
        self.logger.info(f"Loaded {len(df)} records")
        
        # Get processing configuration
        config = self.processing_configs.get(dataset_name, {})
        
        # Apply standard processing
        df = self._standardize_data_types(df, config)
        df = self._clean_text_fields(df, config.get("text_columns", []))
        df = self._parse_dates(df, config.get("date_columns", []))
        df = self._clean_values(df, config.get("value_columns", []))
        df = self._handle_missing_values(df)
        df = self._remove_duplicates(df, config.get("id_columns", []))
        
        # Apply custom processing if provided
        if custom_processing:
            df = custom_processing(df)
        
        # Add processing metadata
        df['_processed_at'] = datetime.now()
        df['_processing_version'] = '1.0'
        
        # Validate processed data
        validation_results = self._validate_data(df, config)
        
        if validation_results['is_valid']:
            # Save processed data
            output_path = self._save_processed_data(dataset_name, df)
            self.logger.info(f"Saved processed data to {output_path}")
        else:
            self.logger.error(f"Validation failed: {validation_results['issues']}")
        
        return df
    
    def _load_latest_data(self, dataset_name: str) -> Optional[pd.DataFrame]:
        """Load the latest raw data file for a dataset."""
        dataset_dir = self.input_dir / dataset_name
        
        if not dataset_dir.exists():
            return None
        
        # Find latest parquet file
        parquet_files = sorted(dataset_dir.glob("*.parquet"), 
                               key=lambda x: x.stat().st_mtime, 
                               reverse=True)
        
        if not parquet_files:
            return None
        
        latest_file = parquet_files[0]
        self.logger.info(f"Loading data from {latest_file}")
        
        return pd.read_parquet(latest_file)
    
    def _standardize_data_types(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """Standardize data types based on configuration."""
        # Ensure ID columns are strings
        for col in config.get("id_columns", []):
            if col in df.columns:
                df[col] = df[col].astype(str).replace('nan', '')
        
        # Ensure text columns are strings
        for col in config.get("text_columns", []):
            if col in df.columns:
                df[col] = df[col].astype(str).replace('nan', '')
        
        return df
    
    def _clean_text_fields(self, df: pd.DataFrame, text_columns: List[str]) -> pd.DataFrame:
        """Clean text fields."""
        for col in text_columns:
            if col in df.columns:
                # Remove extra whitespace
                df[col] = df[col].str.strip()
                df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
                
                # Standardize case for certain fields
                if any(term in col.lower() for term in ['situacao', 'modalidade', 'uf']):
                    df[col] = df[col].str.upper()
        
        return df
    
    def _parse_dates(self, df: pd.DataFrame, date_columns: List[str]) -> pd.DataFrame:
        """Parse and standardize date columns."""
        for col in date_columns:
            if col in df.columns:
                # Try to parse dates
                df[f'{col}_parsed'] = pd.to_datetime(df[col], errors='coerce')
                
                # Log parsing errors
                invalid_dates = df[df[f'{col}_parsed'].isna() & df[col].notna()]
                if len(invalid_dates) > 0:
                    self.logger.warning(
                        f"Failed to parse {len(invalid_dates)} dates in column {col}"
                    )
                
                # Replace original column with parsed version
                df[col] = df[f'{col}_parsed']
                df.drop(f'{col}_parsed', axis=1, inplace=True)
                
                # Extract date components for analysis
                if df[col].notna().sum() > 0:
                    df[f'{col}_year'] = df[col].dt.year
                    df[f'{col}_month'] = df[col].dt.month
                    df[f'{col}_quarter'] = df[col].dt.quarter
                    df[f'{col}_weekday'] = df[col].dt.dayofweek
        
        return df
    
    def _clean_values(self, df: pd.DataFrame, value_columns: List[str]) -> pd.DataFrame:
        """Clean and standardize value columns."""
        for col in value_columns:
            if col in df.columns:
                # Convert to string first for cleaning
                df[col] = df[col].astype(str)
                
                # Remove currency symbols and formatting
                df[col] = df[col].str.replace('R$', '', regex=False)
                df[col] = df[col].str.replace('.', '', regex=False)  # Remove thousand separators
                df[col] = df[col].str.replace(',', '.', regex=False)  # Convert decimal separator
                df[col] = df[col].str.strip()
                
                # Convert to numeric
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Check for negative values
                negative_count = (df[col] < 0).sum()
                if negative_count > 0:
                    self.logger.warning(f"Found {negative_count} negative values in {col}")
                
                # Create additional features
                df[f'{col}_log'] = np.log1p(df[col].fillna(0))
                df[f'{col}_is_zero'] = (df[col] == 0).astype(int)
                
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values based on column type."""
        # For numeric columns, optionally fill with 0 or median
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            missing_pct = df[col].isna().sum() / len(df) * 100
            
            if missing_pct > 0:
                self.logger.info(f"Column {col} has {missing_pct:.1f}% missing values")
                
                # For value columns, missing often means 0
                if 'valor' in col.lower() or 'value' in col.lower():
                    df[col].fillna(0, inplace=True)
        
        # For text columns, fill with empty string
        text_columns = df.select_dtypes(include=['object']).columns
        for col in text_columns:
            df[col].fillna('', inplace=True)
        
        return df
    
    def _remove_duplicates(self, df: pd.DataFrame, id_columns: List[str]) -> pd.DataFrame:
        """Remove duplicate records based on ID columns."""
        if not id_columns:
            # Remove complete duplicates
            before_count = len(df)
            df = df.drop_duplicates()
            after_count = len(df)
            
            if before_count > after_count:
                self.logger.info(f"Removed {before_count - after_count} complete duplicates")
        else:
            # Remove duplicates based on ID columns
            valid_id_cols = [col for col in id_columns if col in df.columns]
            
            if valid_id_cols:
                before_count = len(df)
                df = df.drop_duplicates(subset=valid_id_cols, keep='last')
                after_count = len(df)
                
                if before_count > after_count:
                    self.logger.info(
                        f"Removed {before_count - after_count} duplicates based on {valid_id_cols}"
                    )
        
        return df
    
    def _validate_data(self, df: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate processed data."""
        issues = []
        
        # Check for required columns
        required_columns = (
            config.get("id_columns", []) + 
            config.get("date_columns", []) + 
            config.get("value_columns", [])
        )
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            issues.append(f"Missing required columns: {missing_columns}")
        
        # Check for empty DataFrame
        if len(df) == 0:
            issues.append("DataFrame is empty")
        
        # Check date validity
        for col in config.get("date_columns", []):
            if col in df.columns:
                future_dates = df[df[col] > pd.Timestamp.now()][col].notna().sum()
                if future_dates > 0:
                    issues.append(f"Found {future_dates} future dates in {col}")
        
        # Check value validity
        for col in config.get("value_columns", []):
            if col in df.columns:
                negative_values = (df[col] < 0).sum()
                if negative_values > 0:
                    issues.append(f"Found {negative_values} negative values in {col}")
        
        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "row_count": len(df),
            "column_count": len(df.columns)
        }
    
    def _save_processed_data(self, dataset_name: str, df: pd.DataFrame) -> Path:
        """Save processed data to Parquet format."""
        # Create output directory
        output_dir = self.output_dir / dataset_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{dataset_name}_processed_{timestamp}.parquet"
        output_path = output_dir / filename
        
        # Save to Parquet
        df.to_parquet(
            output_path,
            engine='pyarrow',
            compression='snappy',
            index=False
        )
        
        # Also save data info
        info_path = output_path.with_suffix('.info.json')
        info = {
            "dataset": dataset_name,
            "processed_at": datetime.now().isoformat(),
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": list(df.columns),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "file_size_mb": output_path.stat().st_size / (1024 * 1024)
        }
        
        import json
        with open(info_path, 'w') as f:
            json.dump(info, f, indent=2)
        
        return output_path
    
    def process_all(
        self,
        datasets: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Process all available datasets.
        
        Args:
            datasets: List of dataset names to process (None for all)
            
        Returns:
            Processing summary
        """
        # Get available datasets
        if datasets is None:
            datasets = [d.name for d in self.input_dir.iterdir() 
                       if d.is_dir() and not d.name.startswith('.')]
        
        results = {}
        
        for dataset in datasets:
            self.logger.info(f"\nProcessing {dataset}...")
            
            try:
                df = self.process_dataset(dataset)
                
                results[dataset] = {
                    "status": "success",
                    "rows": len(df),
                    "columns": len(df.columns)
                }
                
            except Exception as e:
                self.logger.error(f"Failed to process {dataset}: {e}")
                results[dataset] = {
                    "status": "failed",
                    "error": str(e)
                }
        
        # Generate summary
        summary = {
            "processed_at": datetime.now().isoformat(),
            "total_datasets": len(results),
            "successful": sum(1 for r in results.values() if r["status"] == "success"),
            "failed": sum(1 for r in results.values() if r["status"] == "failed"),
            "results": results
        }
        
        return summary