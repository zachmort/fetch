import sqlite3
import pandas as pd
from EDA import named_dfs  # Import datasets from EDA.py

# Create an in-memory SQLite database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Load datasets into SQL tables
for file_name, df in named_dfs.items():
    table_name = file_name.replace(".csv", "").lower()  # Normalize table names
    df.to_sql(table_name, conn, index=False, if_exists="replace")
    print(f"Loaded {file_name} into SQL table '{table_name}'")

# Query to find the top 5 brands by receipts scanned among users 21 and over
top5_receipts_query = """
        SELECT 
            p.brand
            , COUNT(t.receipt_id) AS receipt_count
        FROM transaction_takehome t
        JOIN user_takehome u 
            ON t.user_id = u.id
        JOIN products_takehome p 
            ON t.barcode = p.barcode
        WHERE (strftime('%Y', 'now') - strftime('%Y', u.birth_date)) >= 21
            AND p.brand IS NOT NULL
        GROUP BY p.brand
        ORDER BY receipt_count DESC
        LIMIT 5
"""

# Query Execute
top_brands = pd.read_sql_query(top5_receipts_query, conn)


# Query to find the top 5 brands by sales among users that have had their account for at least six months
top5_brands_query = """
        SELECT 
            p.brand
            , SUM(CAST(t.final_sale AS FLOAT)) AS total_sales
        FROM transaction_takehome t
        JOIN user_takehome u 
            ON t.user_id = u.id
        JOIN products_takehome p 
            ON t.barcode = p.barcode
        WHERE u.created_date <= date('now', '-180 days')
            AND p.brand IS NOT NULL
        GROUP BY p.brand
        ORDER BY total_sales DESC
        LIMIT 5
"""

# Query Execute
top_brands_sales = pd.read_sql_query(top5_brands_query, conn)


#### Exploring Data for Dips and salsa
explore_query = """
    WITH TEMP AS (
        SELECT DISTINCT category_3
        FROM products_takehome
        UNION ALL
        SELECT DISTINCT category_2
        FROM products_takehome
        UNION ALL
        SELECT DISTINCT category_1
        FROM products_takehome
    )
    SELECT *
    FROM TEMP
    WHERE category_3 LIKE '%Dip%'
        OR category_3 LIKE '%Dip%'
        OR category_3 LIKE '%Dip%'
"""

explore = pd.read_sql_query(explore_query, conn)

# Query to determine the leading brand in the "Dips & Salsa" category
leading_brand_query = """
        SELECT 
            CASE WHEN p.brand IS NULL THEN 'Unknown' ELSE p.brand END AS brand
            , SUM(CAST(t.final_sale AS FLOAT)) AS total_sales
        FROM transaction_takehome t
        JOIN products_takehome p 
            ON t.barcode = p.barcode
        WHERE p.category_2 = 'Dips & Salsa'
            AND p.brand IS NOT NULL
        GROUP BY p.brand
        ORDER BY total_sales DESC
        LIMIT 1
"""

# Query Execute
leading_brand_dips_salsa = pd.read_sql_query(leading_brand_query, conn)

# Close the database connection
conn.close()
