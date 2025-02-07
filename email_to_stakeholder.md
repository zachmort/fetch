Hey team! I’ve spent the past few days exploring our user and transaction data to understand how everything ties together. I want to share a brief overview of what I’ve found and a request for additional information that will help us move forward and provide more timely and accurate insights. I am also adding an extensive list of the findings/notes below for reference.

1. Key Data Quality Issues & Outstanding Questions
Missing or Invalid Values: A notable number of records in the products.csv have incomplete information (e.g., some brands are labaled as "Unknown" or are left blank) a similar situation occurs in the manufacturer column. It’s unclear if this is expected (e.g., optional fields) or if the data was lost during ingestion. Could you please provid some insight into this?

There are values of "zero" in place of 0s in the receipts quantity column. This compromises the integrity of the data nd prevents mathmatical calculateions from being performaed.

Similar issues in some of the other fields (ie quantity, birthdate) are related to data accuracy issues. We have a user who is reportedly over 125 years old and negative amounts of quantities. Is there any known engineering tests thats these records were left over from?

Unmatched Entries: Certain product IDs found in the transactions data (TRANSACTION_TAKEHOME.csv) don’t have corresponding rows in the products file.

Question: Are these product IDs deprecated, or do we need an updated product list?

Question: Are there known formatting issues in the source systems that cause this mismatch?

Question: Can we set up some time to chat to discuss some other data consistency issue (e.g. similar but duplicative answers for gender, special characters in the manufacturer column, column naming standards) as there are a few other data issues that make analysis a bit complicated.



2. Interesting Trend
A particularly interesting insight from our review is the spike in user activity on weekends:

Transaction volume on Fridays and Saturdays is about 15-20% higher than any other day of the week.
This increase is especially noticable for certain product categories (like snacks or beverages), suggesting a strong weekend purchasing pattern.
This could be leveraged with focused marketing campaigns, inventory planning, special weekend promotions or restocking strategies.

3. Request for Action
To better understand and resolve the data issues:
Validation of Requirements: We need to know which fields are mandatory and which can be legitimately empty.
Updated Data Dictionaries: A current overview of product IDs, user profile fields, and transaction schemas to confirm we’re not missing reference data.
Potential System Logs: If there are logs or error reports from the ingestion process, these might explain how and why data becomes mismatched.
Restricted field entry values: A list of drop down/allowed vales when users sign up/submit receipts would help us understand what to expect and how to control for potential changes in data allowing our pipelines to run without breaking.
Having this additional context and documentation will allow us to confidently filter out irrelevant data, correct potential errors, and focus on meaningful insights—like the weekend purchasing spike—which may guide more informed business decisions.

Thank you for your support, and please let me know if you have any questions!