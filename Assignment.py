import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta

# Function to generate random date (valid and invalid)
def random_date():
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2025, 1, 1)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    
    # Randomly decide whether the date will be valid or invalid (invalid as non-date string)
    if random.random() > 0.9:  
        return "invalid_date_format"
    else:
        return random_date.strftime('%Y-%m-%d')

# Create a list for transaction data
data = []

for _ in range(1,201):
    transaction_id = f"T{random.randint(1, 200)}"  
    user_id = random.randint(1, 10)  
    product_id = random.randint(1001, 1010)  
    price = round(random.uniform(-100, 200),2) if random.random() > 0.2 else np.nan  
    quantity = random.randint(1, 5) 
    timestamp = random_date() 
    
    # Add record to data
    data.append([transaction_id, user_id, product_id, price, quantity, timestamp])


# Create DataFrame
df = pd.DataFrame(data, columns=["transaction_id", "user_id", "product_id", "price", "quantity", "timestamp"])

#Print the DataFrame
print("Original DataFrame:")
print(df)

# Initial row count before making any changes
initial_row_count = len(df)

#To find the duplicates in transaction_id column
duplicates_transaction_id = df[df['transaction_id'].duplicated()]
print("\nDuplicate transaction IDs:")
print(duplicates_transaction_id)
duplicate_record_count = len(duplicates_transaction_id)

# Remove duplicates based on column 'transaction_id'
df = df.drop_duplicates(subset=['transaction_id'])
print("\nThe data after removing duplicates:")
print(df)

# Calculate the median of the 'price' column
median_price = df['price'].median()

# Replace negative values with median
df.loc[df['price'] < 0, 'price'] = median_price

# Replace NaN values with median
df['price'] = df['price'].fillna(median_price)

# cleaned DataFrame with updated 'price' column
print("\nDataFrame with negative and NaN values replaced with median:")
print(df)

# Convert 'timestamp' column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Check if there are invalid timestamps
invalid_timestamps = df[df['timestamp'].isna()]

print("\nRows with invalid timestamps:")
print(invalid_timestamps)

# Replace invalid timestamps with a default valid date
default_date = pd.to_datetime('2022-01-01')
df['timestamp'] = df['timestamp'].fillna(default_date)

print("\nDataFrame after handling invalid timestamps:")
print(df)

# Add new column 'total_value' 
df['total_value'] = df['price'] * df['quantity']

# Print the final DataFrame with 'total_value' column
print("\nDataFrame after adding 'total_value' column:")
print(df)
final_row_count=len(df)

# Print the summary of changes
print("\nSummary of Changes:")
print(f"Initial row count: {initial_row_count}")
print(f"Row count of duplicate values: {duplicate_record_count}")
print(f"Median price used to replace missing prices: {median_price}")
print(f"Final row count after handling all changes: {final_row_count}")


