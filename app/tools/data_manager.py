import os
import pandas as pd
from pathlib import Path
from app.core.logger import setup_logger

logger = setup_logger(__name__)


class DataManager:
    """
    Manages data file loading and validation.
    
    Supports CSV and Excel files (.csv, .xlsx, .xls).
    Provides file info and easy switching between datasets.
    
    Usage:
        dm = DataManager()
        dm.load_file("path/to/data.csv")
        print(dm.get_info_text())
    """
    
    def __init__(self, default_file: str = "data/sample.csv"):
        """
        Initialize DataManager with a default file.
        
        Args:
            default_file: Path to the default data file
        """
        self.current_file = default_file
        self.data_info = None
        self._load_file_info()
    
    def _load_file_info(self):
        """Load and cache information about the current data file."""
        if not os.path.exists(self.current_file):
            logger.warning(f"Default file not found: {self.current_file}")
            self.data_info = None
            return
        
        try:
            df = self._read_file(self.current_file)
            self.data_info = {
                "file": self.current_file,
                "rows": len(df),
                "columns": list(df.columns),
                "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                "size_mb": os.path.getsize(self.current_file) / (1024 * 1024)
            }
            logger.info(f"Loaded file info: {self.current_file}")
        except Exception as e:
            logger.error(f"Error reading file info: {e}")
            self.data_info = None
    
    def _read_file(self, file_path: str) -> pd.DataFrame:
        """
        Read a CSV or Excel file and return as DataFrame.
        
        Args:
            file_path: Path to the file
            
        Returns:
            pandas DataFrame
            
        Raises:
            ValueError: If file format not supported
            Exception: If file cannot be read
        """
        file_lower = file_path.lower()
        
        if file_lower.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_lower.endswith(('.xlsx', '.xls')):
            return pd.read_excel(file_path)
        else:
            raise ValueError(
                f"Unsupported file format: {file_path}. "
                "Supported formats: .csv, .xlsx, .xls"
            )
    
    def load_file(self, file_path: str) -> bool:
        """
        Load a new data file.
        
        Args:
            file_path: Path to the file (can be relative or absolute)
            
        Returns:
            True if successful, False otherwise
        """
        # Handle relative paths
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.getcwd(), file_path)
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
        
        try:
            # Try to read the file to validate it
            df = self._read_file(file_path)
            
            self.current_file = file_path
            self._load_file_info()
            
            logger.info(f"Successfully loaded: {file_path}")
            logger.info(f"Rows: {self.data_info['rows']}, Columns: {len(self.data_info['columns'])}")
            
            return True
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {e}")
            return False
    
    def get_info_text(self) -> str:
        """
        Get a human-readable description of the current data file.
        
        Returns:
            Formatted string with file info
        """
        if not self.data_info:
            return "No data file loaded"
        
        return (
            f"📄 {os.path.basename(self.data_info['file'])}\n"
            f"   Rows: {self.data_info['rows']}\n"
            f"   Columns: {', '.join(self.data_info['columns'])}\n"
            f"   Size: {self.data_info['size_mb']:.2f} MB"
        )
    
    def get_column_info(self) -> dict:
        """
        Get detailed information about columns.
        
        Returns:
            Dictionary with column names and data types
        """
        if not self.data_info:
            return {}
        
        return self.data_info['dtypes']
    
    def get_file_path(self) -> str:
        """
        Get the absolute path to the current data file.
        
        Returns:
            Absolute file path
        """
        return os.path.abspath(self.current_file)
    
    def list_available_files(self, directory: str = "data") -> list:
        """
        List all CSV and Excel files in a directory.
        
        Args:
            directory: Directory to search (default: "data")
            
        Returns:
            List of file paths
        """
        if not os.path.exists(directory):
            logger.warning(f"Directory not found: {directory}")
            return []
        
        supported_extensions = ('.csv', '.xlsx', '.xls')
        files = [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if f.lower().endswith(supported_extensions)
        ]
        
        return sorted(files)
    
    def validate_file(self, file_path: str) -> dict:
        """
        Validate a file without loading it as current file.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            Dictionary with validation results
        """
        result = {
            "valid": False,
            "error": None,
            "info": None
        }
        
        if not os.path.exists(file_path):
            result["error"] = f"File not found: {file_path}"
            return result
        
        try:
            df = self._read_file(file_path)
            result["valid"] = True
            result["info"] = {
                "rows": len(df),
                "columns": list(df.columns),
                "size_mb": os.path.getsize(file_path) / (1024 * 1024)
            }
        except Exception as e:
            result["error"] = str(e)
        
        return result
