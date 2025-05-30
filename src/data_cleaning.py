import re
import os
import pandas as pd
from datetime import datetime
#import ace_tools as tools

def main():
    """Main function to run the data cleaning process."""
    # Get paths to files
    base_dir = os.path.dirname(os.path.dirname(__file__))
    raw_file_path = os.path.join(base_dir, "resources", "data", "Raw-SMS-Meter-tokens.txt")
    csv_output_path = os.path.join(base_dir, "resources", "data", "cleaned_meter_data.csv")
    excel_output_path = os.path.join(base_dir, "resources", "data", "cleaned_meter_data.xlsx")
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(raw_file_path), exist_ok=True)
    
    # Step 1: Load the raw text from the file
    try:
        with open(raw_file_path, "r", encoding="utf-8") as file:
            raw_text = file.read()
    except FileNotFoundError:
        print(f"Error: Raw data file not found at {raw_file_path}")
        print("Please ensure the file exists in the resources/data directory.")
        return
    
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
    print("First 5 rows of cleaned data:")
    print(df_cleaned.head())
    
    # Optional Step: Save the cleaned DataFrame to files
    df_cleaned.to_csv(csv_output_path, index=False)
    df_cleaned.to_excel(excel_output_path, index=False)
    
    print(f"\nCleaned data saved to:")
    print(f"- CSV: {csv_output_path}")
    print(f"- Excel: {excel_output_path}")
    print(f"\nTotal records processed: {len(df_cleaned)}")

if __name__ == "__main__":
    main()