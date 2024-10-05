import pandas as pd

# Load the Excel file
df = pd.read_csv('PSCompPars_2024.10.05_11.19.54.csv')

# Iterate through each row
for index, row in df.iterrows():
    for col_name in df.columns:
        cell_value = row[col_name]  # Accessing each cell value
        print(f"Row {index}, Column {col_name}: {cell_value}")
