import re
import pandas as pd
from datetime import datetime
#import ace_tools as tools

# Step 1: Load the raw text from the uploaded file
with open("Meter-tokens.txt", "r", encoding="utf-8") as file:
    raw_text = file.read()

# Step 2: Extract only the lines that contain token information (those with "Mtr:")
mtr_lines = [line for line in raw_text.splitlines() if "Mtr:" in line]

# Step 3: Define a regular expression pattern to extract data fields
line_pattern = re.compile(
    r"Mtr:(?P<Mtr>\d+)\s+Token:(?P<Token>[\d\-]+)\s+Date:(?P<Date>\d{8})\s(?P<Time>\d{2}:\d{2})\s+"
    r"Units:(?P<Units>[\d.]+)\s+Amt:(?P<Amt>[\d.]+)\s+TknAmt:(?P<TknAmt>[\d.]+)\s+OtherCharges:(?P<OtherCharges>[\d.]+)"
)

# Step 4: Apply the regex pattern to each line and collect the results
parsed_data = []
for line in mtr_lines:
    match = line_pattern.search(line)
    if match:
        entry = match.groupdict()
        # Combine Date and Time into a datetime object
        dt_str = f"{entry['Date']} {entry['Time']}"
        entry['Datetime'] = datetime.strptime(dt_str, "%Y%m%d %H:%M")
        # Remove separate Date and Time after combining
        del entry['Date']
        del entry['Time']
        # Convert string numbers to floats
        for key in ['Units', 'Amt', 'TknAmt', 'OtherCharges']:
            entry[key] = float(entry[key])
        parsed_data.append(entry)

# Step 5: Create a DataFrame from the parsed data
df_cleaned = pd.DataFrame(parsed_data)

# Optional Step: Display the DataFrame to the user
print(df_cleaned.head())

# Optional Step: Save the cleaned DataFrame to a CSV file
df_cleaned.to_csv("cleaned_meter_data.csv", index=False)
# Optional Step: Save the cleaned DataFrame to an Excel file
df_cleaned.to_excel("cleaned_meter_data.xlsx", index=False)