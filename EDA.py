### Findings
### 1. Missing values: There are missing values in the datasets.
### 2. Duplicate rows: There are no duplicate rows in the datasets.
### 3. Data types: The data types of the columns in the datasets are as follows:

import pandas as pd
import os
from typing import List, Any, Dict

# loop through file names in folder path
csv_files: List[str] = [f for f in os.listdir('.') if f.endswith('.csv')]

# Read each CSV file and store it in a dictionary with file names as keys
named_dfs: Dict[str, pd.DataFrame] = {}

for file in csv_files:
    df: pd.DataFrame = pd.read_csv(file)
    named_dfs[file] = df  # Associate filename with DataFrame
    print(f"Successfully read: {file}")
    print(f"Shape: {df.shape}")
    assert df.shape[0] > 0, f"Empty dataframe: {file}"
    print(f"Columns: {df.columns.tolist()}\n")

def check_duplicates(dfs: Dict[str, pd.DataFrame]) -> Dict[str, int]:
    """Check for duplicate rows in each datasets.
    
    Args:
        *dfs: Variable number of pandas DataFrames in a list.
    Returns:
        Dict[str, int]: Dictionary with duplicate row counts for each DataFrame.
    """
    duplicate_counts: dict[Any, Any] = {}
    for i, df in dfs.items():
        duplicate_counts[f'{i}'] = df.duplicated().sum()
    return duplicate_counts

def check_data_types(dfs: Dict[str, pd.DataFrame]) -> Dict[str, pd.Series]:
    """Return the data types of each column in each datasets.
    
    Args:
        *dfs: Variable number of pandas DataFrames in a list.
    Returns:
        Dict[str, pd.Series]: Dictionary with column data types for each DataFrame.
    """
    data_types: dict[Any, Any] = {}
    for i, df in dfs.items():
        data_types[f'{i}'] = df.dtypes
    return data_types

def check_key_integrity(transactions_df: pd.DataFrame, products_df: pd.DataFrame, users_df: pd.DataFrame) -> Dict[str, int]:
    """Check for missing product and user IDs in transactions.
    
    Args:
        transactions_df: Transactions DataFrame.
        products_df: Products DataFrame.
        users_df: Users DataFrame.
    Returns:
        Dict[str, int]: Dictionary with counts of missing product and user IDs.
    """
    missing_product_ids: int = transactions_df[~transactions_df['BARCODE'].isin(products_df['BARCODE'])]['BARCODE'].nunique()
    missing_user_ids: int = transactions_df[~transactions_df['USER_ID'].isin(users_df['ID'])]['USER_ID'].nunique()

    return {
        "missing_product_ids_in_transactions": missing_product_ids,
        "missing_user_ids_in_transactions": missing_user_ids,
    }

def check_missing_values(dfs: dict[str,pd.DataFrame]) -> Dict[str, pd.Series]:
    """Check for missing values in multiple datasets.
    
    Args:
        *dfs: Variable number of pandas DataFrames.
    Returns:
        Dict[str, pd.Series]: Dictionary with missing value counts for each DataFrame.
    """
    missing_values = {}
    for i, df in dfs.items():
        missing_values[f'{i}'] = df.isnull().sum()
    return missing_values


if __name__ == "__main__":
    transactions_df = named_dfs.get("TRANSACTION_TAKEHOME.csv")
    products_df = named_dfs.get("PRODUCTS_TAKEHOME.csv")
    users_df = named_dfs.get("USER_TAKEHOME.csv")

    # Check if datasets exist before proceeding (to avoid errors)
    if transactions_df is not None and products_df is not None and users_df is not None:
        key_integrity_issues: Dict[str, int] = check_key_integrity(transactions_df, products_df, users_df)
    else:
        key_integrity_issues = "Missing required datasets."

    print("\n checking for missing values")
    missing_values = check_missing_values(named_dfs)
    print("\n checking for duplicates")
    duplicate_counts: Dict[str, int] = check_duplicates(named_dfs)
    print("\n checking for data types")
    data_types = check_data_types(named_dfs)

    print(
        {
        "missing_values": missing_values,
        "duplicate_counts": duplicate_counts,
        "data_types": data_types,
        "key_integrity_issues": key_integrity_issues,
    }
    )