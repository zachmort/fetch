import sqlite3
import pandas as pd
from EDA import named_dfs  # Import datasets from EDA.py

# Create an in-memory SQLite database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Load datasets into SQL tables
for file_name, df in named_dfs.items():
    table_name = file_name.replace(".csv", "").lower()  # Normalize table names
    df.to_sql(table_name, conn, index=False, if_exists="replace") #Creates a table in the database with the name of the dataframe
    print(f"Loaded {file_name} into SQL table '{table_name}'")

# Query looking into the transaction_takehome table and the duplicate reciepts in the data
receipts_query = """        
        SELECT 
            receipt_id
            , barcode
            , user_id
            , COUNT(*) AS record_count
        FROM transaction_takehome t
        GROUP BY receipt_id, barcode, user_id
        HAVING COUNT(*) < 2
"""

# Query Execute
print("receipts_query check")
receipts_explore = pd.read_sql_query(receipts_query, conn)

# Query to find the top 5 brands by receipts scanned among users 21 and over
# Looking for count of receipts scanned (There is duplicates in the data so we are counting distinct receipts)
# Assuming we dont want brands with null values
# Assuming brand is referring to the brand of the product not store brand
top5_receipts_query = """
        WITH TEMP AS (
            SELECT DISTINCT 
                receipt_id
                , barcode
                , user_id
            FROM transaction_takehome
        )
        SELECT 
            p.brand
            , COUNT(DISTINCT t.receipt_id) AS receipt_count
        FROM TEMP t
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
print(top_brands)

# Answer to the question: The top 5 brands by distinct receipts scanned among users 21 and over are:
# These counts reflect distinct receipts and exclude any brands with NULL values, aligning with the assumption that “brand” refers to the product’s brand rather than the store’s.
# NERDS CANDY (3 receipts)
# DOVE (3 receipts)
# TRIDENT (2 receipts)
# SOUR PATCH KIDS (2 receipts)
# MEIJER (2 receipts)


# Query to find the top 5 brands by sales among users that have had their account for at least six months
# Assuming we dont want brands with null values
# Assuming we dont want receipts with NULL values
# Assuming final_sale means the final price of the order rather than the price of the item
## Assuming quantity cant be a decimal so rounding all decimals down to 0th place
# Assuming we want to remove "duplicate" receipts (receipts with the same items) and take the max or the sales prices and quantities
top5_brands_query = """
        WITH TEMP AS (
            SELECT 
                receipt_id
                , barcode
                , user_id
                , MAX(CAST(CASE WHEN final_sale IS NULL THEN 0 ELSE final_sale END AS final_sale)) AS final_sale
                , MAX(ROUND(CASE WHEN LOWER(final_quantity) = "zero" THEN 0 ELSE final_quantity END,0)) AS final_quantity
            FROM transaction_takehome
            GROUP BY receipt_id, barcode, user_id
        )
        SELECT
            p.brand
            , SUM(t.final_sale) AS total_sales
            , SUM(t.final_quantity) AS total_items_sold
        FROM TEMP t
        JOIN user_takehome u 
            ON t.user_id = u.id
        JOIN products_takehome p 
            ON t.barcode = p.barcode
        WHERE u.created_date >= date(u.created_date, '-180 days')
            AND p.brand IS NOT NULL
        GROUP BY p.brand
        ORDER BY total_sales DESC
        LIMIT 5
"""

# Query Execute
top_brands_sales = pd.read_sql_query(top5_brands_query, conn)
print(top_brands_sales)

# Answer to the question: The top 5 brands by total sales among users with accounts older than six months are:
# CVS (USD 72.00 total sales, 1 item sold)
# DOVE (USD 30.91 total sales, 3 items sold)
# TRIDENT (USD 23.36 total sales, 2 items sold)
# COORS LIGHT (USD 17.48 total sales, 1 item sold)
# TRESEMMÉ (USD 14.58 total sales, 2 items sold)



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
print(explore)

# Query to determine the leading brand in the "Dips & Salsa" category
# Assuming "Dips & Salsa" is a the subcategory we want and not just a all encompassing category that would include other items (like bean dip, cheese dip etc)
# How does 1 define leading brand? Is it the brand with the most sales, the most receipts scanned, most unique users, most consistent purchases (ie users constantly come back to the brand rather than just a large influx in 1 month while while other months struggle) or something else?
# From Fetch's perspective, leading brand could be a brand with the most individual receipts scanned as this would provide data for more than just items purchased but would also provide frequency of shopping, consumer habits, complimentary goods purchased etc.
leading_brand_query = """
        SELECT 
            CASE WHEN p.brand IS NULL THEN 'Unknown' ELSE p.brand END AS brand
            , COUNT(DISTINCT receipt_id) AS distinct_sales
        FROM transaction_takehome t
        JOIN products_takehome p 
            ON t.barcode = p.barcode
        WHERE p.category_2 = 'Dips & Salsa'
            AND p.brand IS NOT NULL
        GROUP BY p.brand
        ORDER BY distinct_sales DESC
        LIMIT 5
"""

# Query Execute
leading_brand_dips_salsa = pd.read_sql_query(leading_brand_query, conn)
print(leading_brand_dips_salsa)

# Answer to the question: Which is the leading brand in the Dips & Salsa category?
# TOSTITOS – 36 distinct sales
# PACE – 24 distinct sales
# FRITOS – 19 distinct sales
# DEAN'S DAIRY DIP – 17 distinct sales
# MARKETSIDE – 16 distinct sales


# Close the database connection
conn.close()
