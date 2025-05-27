"""
Data collection module for automated and incremental data fetching.
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable, Union
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from tqdm import tqdm

from src.api.client import TransparenciaAPIClient


class DataCollector:
    """
    Automated data collector for Portal da Transparência.
    
    Features:
    - Incremental data collection
    - Progress tracking and resumption
    - Efficient storage in Parquet format
    - Comprehensive logging
    - Error handling and retry logic
    """
    
    def __init__(self, output_dir: str = "data/raw"):
        """
        Initialize data collector.
        
        Args:
            output_dir: Directory to save collected data
        """
        self.client = TransparenciaAPIClient()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Collection state management
        self.state_file = self.output_dir / ".collection_state.json"
        self.state = self._load_state()
    
    def _load_state(self) -> Dict[str, Any]:
        """Load collection state from file."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading state: {e}")
        
        return {
            "collections": {},
            "last_update": None
        }
    
    def _save_state(self) -> None:
        """Save collection state to file."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Error saving state: {e}")
    
    def collect_endpoint(
        self,
        endpoint_name: str,
        fetch_method: Callable,
        params: Optional[Dict[str, Any]] = None,
        max_pages: Optional[int] = None,
        page_size: int = 500,
        incremental: bool = True,
        date_field: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Collect data from a specific endpoint.
        
        Args:
            endpoint_name: Name of the endpoint for tracking
            fetch_method: API client method to fetch data
            params: Additional parameters for the API call
            max_pages: Maximum number of pages to fetch
            page_size: Number of records per page
            incremental: Whether to perform incremental collection
            date_field: Field to use for incremental updates
            
        Returns:
            Collection statistics
        """
        self.logger.info(f"Starting collection for {endpoint_name}")
        
        # Initialize collection stats
        stats = {
            "endpoint": endpoint_name,
            "start_time": datetime.now(),
            "records_collected": 0,
            "pages_collected": 0,
            "errors": 0,
            "status": "in_progress"
        }
        
        # Prepare parameters
        params = params or {}
        
        # Check for incremental collection
        if incremental and endpoint_name in self.state.get("collections", {}):
            last_collection = self.state["collections"][endpoint_name]
            if date_field and "last_date" in last_collection:
                # Add date filter for incremental collection
                params[f"{date_field}Inicial"] = last_collection["last_date"]
                self.logger.info(f"Incremental collection from {last_collection['last_date']}")
        
        # Collect data with pagination
        all_records = []
        page = 1
        
        try:
            with tqdm(desc=f"Collecting {endpoint_name}") as pbar:
                while True:
                    try:
                        # Set pagination parameters
                        params["pagina"] = page
                        params["quantidade"] = page_size
                        
                        # Fetch data
                        self.logger.debug(f"Fetching page {page}")
                        records = fetch_method(**params)
                        
                        if not records:
                            self.logger.info(f"No more records at page {page}")
                            break
                        
                        all_records.extend(records)
                        stats["records_collected"] += len(records)
                        stats["pages_collected"] += 1
                        
                        # Update progress
                        pbar.update(len(records))
                        pbar.set_postfix({
                            "page": page,
                            "total": stats["records_collected"]
                        })
                        
                        # Check if we've reached max pages
                        if max_pages and page >= max_pages:
                            self.logger.info(f"Reached maximum pages ({max_pages})")
                            break
                        
                        page += 1
                        
                    except Exception as e:
                        self.logger.error(f"Error on page {page}: {e}")
                        stats["errors"] += 1
                        
                        # Skip to next page on error
                        if stats["errors"] > 5:
                            self.logger.error("Too many errors, stopping collection")
                            stats["status"] = "failed"
                            break
                        
                        page += 1
            
            # Save collected data
            if all_records:
                output_file = self._save_data(endpoint_name, all_records)
                stats["output_file"] = str(output_file)
                stats["status"] = "completed"
                
                # Update state
                self.state["collections"][endpoint_name] = {
                    "last_collection": datetime.now().isoformat(),
                    "records_collected": stats["records_collected"],
                    "last_page": page - 1
                }
                
                # Track last date if available
                if date_field and all_records:
                    df = pd.DataFrame(all_records)
                    if date_field in df.columns:
                        last_date = df[date_field].max()
                        self.state["collections"][endpoint_name]["last_date"] = str(last_date)
                
                self.state["last_update"] = datetime.now().isoformat()
                self._save_state()
                
        except Exception as e:
            self.logger.error(f"Fatal error during collection: {e}")
            stats["status"] = "failed"
            stats["error_message"] = str(e)
        
        # Calculate duration
        stats["end_time"] = datetime.now()
        stats["duration"] = (stats["end_time"] - stats["start_time"]).total_seconds()
        
        self.logger.info(
            f"Collection completed: {stats['records_collected']} records "
            f"in {stats['duration']:.2f} seconds"
        )
        
        return stats
    
    def _save_data(self, endpoint_name: str, records: List[Dict[str, Any]]) -> Path:
        """
        Save collected data to Parquet format.
        
        Args:
            endpoint_name: Name of the endpoint
            records: List of records to save
            
        Returns:
            Path to saved file
        """
        # Convert to DataFrame
        df = pd.DataFrame(records)
        
        # Add metadata columns
        df['_collected_at'] = datetime.now()
        df['_endpoint'] = endpoint_name
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{endpoint_name}_{timestamp}.parquet"
        output_path = self.output_dir / endpoint_name / filename
        
        # Create directory if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to Parquet with compression
        df.to_parquet(
            output_path,
            engine='pyarrow',
            compression='snappy',
            index=False
        )
        
        self.logger.info(f"Saved {len(records)} records to {output_path}")
        
        # Also save a sample as JSON for easy inspection
        sample_path = output_path.with_suffix('.sample.json')
        with open(sample_path, 'w', encoding='utf-8') as f:
            json.dump(records[:5], f, ensure_ascii=False, indent=2, default=str)
        
        return output_path
    
    def collect_all(
        self,
        endpoints: Optional[List[str]] = None,
        incremental: bool = True,
        max_pages_per_endpoint: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Collect data from multiple endpoints.
        
        Args:
            endpoints: List of endpoint names to collect (None for all)
            incremental: Whether to perform incremental collection
            max_pages_per_endpoint: Maximum pages per endpoint
            
        Returns:
            Collection statistics for all endpoints
        """
        # Define available collections
        available_collections = {
            "orgaos": {
                "method": self.client.get_orgaos,
                "params": {"sistema": "siafi"},
                "date_field": None
            },
            "contratos": {
                "method": self.client.get_contratos,
                "params": {},
                "date_field": "dataAssinatura"
            },
            "convenios": {
                "method": self.client.get_convenios,
                "params": {},
                "date_field": "dataAssinatura"
            },
            "pagamentos": {
                "method": self.client.get_pagamentos,
                "params": {},
                "date_field": "data"
            },
            "licitacoes": {
                "method": self.client.get_licitacoes,
                "params": {},
                "date_field": "dataAbertura"
            },
            "fornecedores": {
                "method": self.client.get_fornecedores,
                "params": {},
                "date_field": None
            }
        }
        
        # Select endpoints to collect
        if endpoints:
            collections_to_run = {
                k: v for k, v in available_collections.items() 
                if k in endpoints
            }
        else:
            collections_to_run = available_collections
        
        # Run collections
        results = {}
        
        for endpoint_name, config in collections_to_run.items():
            self.logger.info(f"\nCollecting {endpoint_name}...")
            
            try:
                stats = self.collect_endpoint(
                    endpoint_name=endpoint_name,
                    fetch_method=config["method"],
                    params=config["params"],
                    max_pages=max_pages_per_endpoint,
                    incremental=incremental,
                    date_field=config["date_field"]
                )
                results[endpoint_name] = stats
                
            except Exception as e:
                self.logger.error(f"Failed to collect {endpoint_name}: {e}")
                results[endpoint_name] = {
                    "status": "failed",
                    "error": str(e)
                }
        
        # Generate summary
        summary = {
            "total_endpoints": len(results),
            "successful": sum(1 for r in results.values() if r.get("status") == "completed"),
            "failed": sum(1 for r in results.values() if r.get("status") == "failed"),
            "total_records": sum(r.get("records_collected", 0) for r in results.values()),
            "collection_time": datetime.now().isoformat(),
            "results": results
        }
        
        # Save summary
        summary_file = self.output_dir / f"collection_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2, default=str)
        
        return summary
    
    def get_collection_status(self) -> Dict[str, Any]:
        """Get status of all collections."""
        status = {
            "last_update": self.state.get("last_update"),
            "endpoints": {}
        }
        
        for endpoint, info in self.state.get("collections", {}).items():
            # Check for existing files
            endpoint_dir = self.output_dir / endpoint
            files = list(endpoint_dir.glob("*.parquet")) if endpoint_dir.exists() else []
            
            status["endpoints"][endpoint] = {
                "last_collection": info.get("last_collection"),
                "records_collected": info.get("records_collected", 0),
                "files_count": len(files),
                "total_size_mb": sum(f.stat().st_size for f in files) / (1024 * 1024) if files else 0
            }
        
        return status
    
    def clean_old_data(self, days_to_keep: int = 30) -> Dict[str, int]:
        """
        Clean old data files.
        
        Args:
            days_to_keep: Number of days to keep data
            
        Returns:
            Cleanup statistics
        """
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cleanup_stats = {}
        
        for endpoint_dir in self.output_dir.iterdir():
            if not endpoint_dir.is_dir() or endpoint_dir.name.startswith('.'):
                continue
            
            deleted_count = 0
            deleted_size = 0
            
            for file in endpoint_dir.glob("*.parquet"):
                # Check file age
                file_time = datetime.fromtimestamp(file.stat().st_mtime)
                
                if file_time < cutoff_date:
                    file_size = file.stat().st_size
                    file.unlink()
                    
                    # Also remove sample file if exists
                    sample_file = file.with_suffix('.sample.json')
                    if sample_file.exists():
                        sample_file.unlink()
                    
                    deleted_count += 1
                    deleted_size += file_size
            
            if deleted_count > 0:
                cleanup_stats[endpoint_dir.name] = {
                    "files_deleted": deleted_count,
                    "size_freed_mb": deleted_size / (1024 * 1024)
                }
        
        self.logger.info(f"Cleanup completed: {cleanup_stats}")
        return cleanup_stats