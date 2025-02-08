# Importing required libraries
import pandas as pd
import os
from typing import List, Any, Dict
import matplotlib.pyplot as plt
import seaborn as sns

# loop through file names in folder path
csv_files: List[str] = [f for f in os.listdir('.') if f.endswith('.csv')]

# Read each CSV file and store it in a dictionary with file names as keys
named_dfs: Dict[str, pd.DataFrame] = {}

for file in csv_files:
    try:
        df: pd.DataFrame = pd.read_csv(file)
        named_dfs[file] = df  # link filename with DataFrame
        print(f"Successfully read: {file}")
        print(f"Shape: {df.shape}")
        assert df.shape[0] > 0, f"Empty dataframe: {file}" #assert that the dataframe is not empty
        print(f"Columns: {df.columns.tolist()}\n")
    except Exception as e:
        print(f"Error reading {file}: {e}")


# Get high level info on each dataset
print(named_dfs['TRANSACTION_TAKEHOME.csv'].info())
print(named_dfs['PRODUCTS_TAKEHOME.csv'].info())
print(named_dfs['USER_TAKEHOME.csv'].info())

# Get descriptive statistics for each dataset
print(named_dfs['TRANSACTION_TAKEHOME.csv'].describe())
print(named_dfs['PRODUCTS_TAKEHOME.csv'].describe())
print(named_dfs['USER_TAKEHOME.csv'].describe())

# Create functions to check for missing values, duplicates, data types, and key integrity
# Using function for reusability, although it is not necessary for this small dataset
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
    missing_values   = {}
    for i, df in dfs.items():
        missing_values[f'{i}'] = df.isnull().sum()
    return missing_values


# Function to visualize CSV data
def visualize_csv_data(csv_files: dict) -> None:
    """
    Loops through all CSV datasets and generates bar charts 
    showing the top 5 most frequent values in each column.

    Args:
        csv_files (dict): Dictionary where keys are file names 
                          and values are DataFrames.

    Returns:
        None (displays visualizations).
    """
    for file_name, df in csv_files.items():
        print(f"Visualizing: {file_name}")

        # Paass if df is empty
        if df.empty:
            print(f"{file_name} is empty. Skipping.\n")
            continue

        for col in df.columns:
            # Get the top 5 most frequent values (including NaN as a category)
            top_5 = df[col].value_counts(dropna=False).head(5)

            # Plot a bar chart of the top 5 vaues in each column by frequency
            plt.figure(figsize=(8, 4))
            sns.barplot(x=top_5.index.astype(str), y=top_5.values, palette="Blues_d")
            plt.title(f"Top 5 Frequent Values in '{col}' - {file_name}")
            plt.xlabel("Value")
            plt.ylabel("Frequency")
            plt.xticks(rotation=30, ha="right")  # tilt x-labels for readability
            plt.tight_layout()
            plt.show()

        print(f"Finished visualizing {file_name}\n")


# Only run the following code if the script is executed directly
if __name__ == "__main__":
    transactions_df: pd.DataFrame | None = named_dfs.get("TRANSACTION_TAKEHOME.csv")
    products_df: pd.DataFrame | None = named_dfs.get("PRODUCTS_TAKEHOME.csv")
    users_df: pd.DataFrame | None = named_dfs.get("USER_TAKEHOME.csv")

    # Check if datasets exist before proceeding (to avoid errors)
    if transactions_df is not None or products_df is not None or users_df is not None:
        key_integrity_issues: Dict[str, int] | str = check_key_integrity(transactions_df, products_df, users_df)
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

    # # Call the viz function with the datasets
    visualize_csv_data({
        "PRODUCTS_TAKEHOME.csv": products_df,
        "TRANSACTION_TAKEHOME.csv": transactions_df,
        "USER_TAKEHOME.csv": users_df,
    })