### Findings ###
# Are there any data quality issues present?
# - Missing data in the 'PRODUCTS_TAKEHOME.csv' dataset.
# - Duplicate rows in the 'TRANSACTION_TAKEHOME.csv' dataset.
# - Missing product and user IDs in the 'TRANSACTION_TAKEHOME.csv' dataset.
# In products csv the manufacturer column has missing values but also has values for "placeholder manufacturer" which could be confusing as if the manufacturer is truly unknown all values should have the place holder or be NULL/Nan.
# In products csv the brand column has missing values but also has values for "unknown brand" which could be confusing as if the brand is truly unknown all values should have the place holder or be NULL/Nan.
# Not necessary but any primary/forgien keys could be moved towards the font of the datasets for easier reference
# Barcodes are missing in the products csv
# Scan date in transactions csv is a datetime value rather than a date value
# Also scan date is in UTC time zone which could be confusing if the data is not intended to be in UTC
# Birth date in users csv is a datetime value rather than a date value
# Store name in Transactions csv sometimes contains the store number, special characters and store name in the same record
# Receipt id contains dupes in transactions csv, generally these should be unique but have differing final_quantity and final_sale values
# Final quantity contains string values in transactions csv (which should be numeric/integer assuming it is the quantity of the product)
# Final quantity contains "extremely high" values in transactions csv (276 for example)
# created date and birth date in users csv is a datetime value rather than a date value, as well as being in UTC time zone
# User gender has values of (prefer not to say, prefer_not_to_say) + (unknown, NULL) + (non_binary, non-binary) which could be viewed as duplicative
# Extreme values of birthdate in users csv (1901) and (2015) which could be errors or during the user sign up process restrictions were not put in place for a min/max age
# barcode contains -1 values in products csv which could be an error or a placeholder value (maybe engineering test cases)
# Manufacturer contains suffixes like llc, inc, co, etc. which could be removed for consistency

# Are there any fields that are challenging to understand?
# - The 'final_sale' column in the 'TRANSACTION_TAKEHOME.csv' dataset is not clear. Final quantity shows "zero" for quantity but final sale has positive dollar amounts
# - The 'category_1', 'category_2', and 'category_3' columns in the 'PRODUCTS_TAKEHOME.csv' dataset are not self-explanatory.
# - The 'created_date' column in the 'USER_TAKEHOME.csv' dataset is not clear.
# Receipt id contains dupes in transactions csv, generally these should be unique but have differing final_quantity and final_sale values
# Language in the datasets is not consistent, for example in the products csv the manufacturer column has missing values but also has values for "placeholder manufacturer" which could be confusing as if the manufacturer is truly unknown all values should have the place holder or be NULL/Nan.
# language for the user contains values "en" but also "es-419" so it is difficult to understand what the "-419" means and why a suffix is not also on "en" values
# Reciept id I would assume would be unique since it is in the trasnactions csv and you get 1 reciept per transaction, but there are duplicates in the dataset
# Final quantity contains decimal values which seems unlikely for a quantity of a product
# The category granularity is not clear, for example in the products csv the category_1, category_2, and category_3 columns in the 'PRODUCTS_TAKEHOME.csv' dataset are not self-explanatory
# Is state in User csv the state of the user or the state of the store they shop at? This could be confusing if the data is not intended to be the state of the user




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

# # Call the function with the datasets
visualize_csv_data({
    "PRODUCTS_TAKEHOME.csv": products_df,
    "TRANSACTION_TAKEHOME.csv": transactions_df,
    "USER_TAKEHOME.csv": users_df,
})
