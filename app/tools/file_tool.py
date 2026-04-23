import os
import pandas as pd
from app.core.logger import setup_logger

logger = setup_logger(__name__)

def read_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return "Error: File not found"

    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
            logger.info(f"Loaded CSV file: {file_path}")
            return df.head().to_string()

        elif file_path.endswith(".txt"):
            with open(file_path, "r") as f:
                content = f.read()
            logger.info(f"Loaded TXT file: {file_path}")
            return content[:1000]

        else:
            logger.warning(f"Unsupported file type: {file_path}")
            return "Error: Unsupported file type"

    except Exception as e:
        logger.exception("Error reading file")
        return str(e)