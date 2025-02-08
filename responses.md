# First: Explore the data
### The python code can be found with the documentation, notes and EDA in the EDA.py file
*Are there any data quality issues present?*
- In products csv the manufacturer column has missing values but also has values for "placeholder manufacturer" which could be confusing as if the manufacturer is truly unknown all values should have the place holder or be NULL/Nan
- In products csv the brand column has missing values but also has values for "unknown brand" which could be confusing as if the brand is truly unknown all values should have the place holder or be NULL/Nan
- The are no "true" primary keys in the transactions as the receipt id is not unique
- Not necessary but any primary/foreign keys could be moved towards the font of the datasets for easier reference
- Barcodes are missing in the products csv
- Scan date in transactions csv is a datetime value rather than a date value
- Also scan date is in UTC time zone which could be confusing if the data is not intended to be in UTC
- Birth date in users csv is a datetime value rather than a date value
- Store name in Transactions csv sometimes contains the store number, special characters and store name in the same record
- Receipt id contains dupes in transactions csv, generally these should be unique but have differing final_quantity and final_sale values
- Final quantity contains string values in transactions csv (which should be numeric/integer assuming it is the quantity of the product)
- Final quantity contains "extremely high" values in transactions csv (276 for example)
- created date and birth date in users csv is a datetime value rather than a date value, as well as being in UTC time zone
- User gender has values of (prefer not to say, prefer_not_to_say) + (unknown, NULL) + (non_binary, non-binary) which could be viewed as duplicative
- Extreme values of birthdate in users csv (1901) and (2015) which could be errors or during the user sign up process restrictions were not put in place for a min/max age
- barcode contains -1 values in products csv which could be an error or a placeholder value (maybe engineering test cases)
- Manufacturer contains suffixes like llc, inc, co, etc. which could be removed for consistency
- category columns contain special characters (e.g. /, &) which could be removed for consistency
- Is the final sale amount in the transactions csv in USD or another currency?
- Is the final sale amount the amount per item or the total amount for the transaction?

*Are there any fields that are challenging to understand?*
- The 'final_sale' column in the 'TRANSACTION_TAKEHOME.csv' dataset is not clear. Final quantity shows "zero" for quantity but final sale has positive dollar amounts
- The 'category_1', 'category_2', and 'category_3' columns in the 'PRODUCTS_TAKEHOME.csv' dataset are not self-explanatory
- The 'created_date' column in the 'USER_TAKEHOME.csv' dataset is not clear
- Receipt id contains dupes in transactions csv, generally these should be unique but have differing final_quantity and final_sale values
- Language in the datasets is not consistent, for example in the products csv the manufacturer column has missing values but also has values for "placeholder manufacturer" which could be confusing as if the manufacturer is truly unknown all values should have the place holder or be NULL/Nan
- language for the user contains values "en" but also "es-419" so it is difficult to understand what the "-419" means and why a suffix is not also on "en" values
- Receipt id I would assume would be unique since it is in the transactions csv and you get 1 Receipt per transaction, but there are duplicates in the dataset
- Final quantity contains decimal values which seems unlikely for a quantity of a product
- The category granularity is not clear, for example in the products csv the category_1, category_2, and category_3 columns in the 'PRODUCTS_TAKEHOME.csv' dataset are not self-explanatory
- Is state in User csv the state of the user or the state of the store they shop at? This could be confusing if the data is not intended to be the state of the user
- (Confusing as well as data quality issue) In products csv the manufacturer column has missing values but also has values for "placeholder manufacturer" which could be confusing as if the manufacturer is truly unknown all values should have the place holder or be NULL/Nan
- (Confusing as well as data quality issue) In products csv the brand column has missing values but also has values for "unknown brand" which could be confusing as if the brand is truly unknown all values should have the place holder or be NULL/Nan


# Provide SQL Queries
### The SQL queries can be found with the assumptions, notes and EDA in the SQLExplore.py file

### Answer to the question: The top 5 brands by distinct receipts scanned among users 21 and over are:
### These counts reflect distinct receipts and exclude any brands with NULL values, aligning with the assumption that “brand” refers to the product’s brand rather than the store’s.

1. NERDS CANDY (3 receipts)
2. DOVE (3 receipts)
3. TRIDENT (2 receipts)
4. SOUR PATCH KIDS (2 receipts)
5. MEIJER (2 receipts)


### Answer to the question: The top 5 brands by total sales among users with accounts older than six months are:
1. CVS (USD 72.00 total sales, 1 item sold)
2. DOVE (USD 30.91 total sales, 3 items sold)
3. TRIDENT (USD 23.36 total sales, 2 items sold)
4. COORS LIGHT (USD 17.48 total sales, 1 item sold)
5. TRESEMMÉ (USD 14.58 total sales, 2 items sold)


### Answer to the question: Which is the leading brand in the Dips & Salsa category?
1. TOSTITOS – 36 distinct sales
2. PACE – 24 distinct sales
3. FRITOS – 19 distinct sales
4. DEAN'S DAIRY DIP – 17 distinct sales
5. MARKETSIDE – 16 distinct sales

# Third: communicate with stakeholders
Hey team! I’ve spent the past few days exploring our user and transaction data to understand how everything ties together. I want to share a brief overview of what I’ve found and a request for additional information that will help us move forward and provide more timely and accurate insights. I am also adding an extensive list of the findings/notes below for reference.

1. ### Key Data Quality Issues & Outstanding Questions
#### A. Key Data Quality Issues
- Missing or Invalid Values: A notable number of records in the products.csv have incomplete information (e.g., some brands are labeled as "Unknown" or are left blank) a similar situation occurs in the manufacturer column. It’s unclear if this is expected (e.g., optional fields) or if the data was lost during ingestion. Could you please provid some insight into this?
- There are values of "zero" in place of 0s in the receipts quantity column. This compromises the integrity of the data nd prevents mathematical calculations from being performed.
- Similar issues in some of the other fields (ie quantity, birthdate) are related to data accuracy issues. We have a user who is reportedly over 125 years old and negative amounts of quantities. Is there any known engineering tests thats these records were left over from?
- Unmatched Entries: Certain product IDs found in the transactions data (TRANSACTION_TAKEHOME.csv) don’t have corresponding rows in the products file.

#### B. Key Data Quality Issues
- Question: Are these product IDs deprecated, or do we need an updated product list?
- Question: Are there known formatting issues in the source systems that cause this mismatch?
- Question: For the sales amounts are the amounts on a per item basis or a total amount for all items and as a follow up are the amount in USD?
- Question: Can we set up some time to chat to discuss some other data consistency issue (e.g. similar but duplicative answers for gender, special characters in the manufacturer column, column naming standards) as there are a few other data issues that make analysis a bit complicated.



2. ### Interesting Trend
A particularly interesting insight from our review is the spike in user activity on weekends:
- Transaction volume on *Fridays and Saturdays* is about *15-20% higher* than any other day of the week.
This increase is especially noticeable for certain product categories (like snacks or beverages), suggesting a strong weekend purchasing pattern.
This could be leveraged with focused marketing campaigns, inventory planning, special weekend promotions or restocking strategies.

3. ### Request for Action
To better understand and resolve the data issues:
- Validation of Requirements: We need to know which fields are mandatory and which can be legitimately empty.
- Updated Data Dictionaries: A current overview of product IDs, user profile fields, and transaction schemas to confirm we’re not missing reference data.
- Potential System Logs: If there are logs or error reports from the ingestion process, these might explain how and why data becomes mismatched.
- Restricted field entry values: A list of drop down/allowed vales when users sign up/submit receipts would help us understand what to expect and how to control for potential changes in data allowing our pipelines to run without breaking.
- Having this additional context and documentation will allow us to confidently filter out irrelevant data, correct potential errors, and focus on meaningful insights—like the weekend purchasing spike—which may guide more informed business decisions.

Thank you for your support, and please let me know if you have any questions!