"""
Token visualization tool to analyze and display token data graphically.
This addresses the "Future Enhancement" mentioned in the README: 
"Visualize token data using charts and graphs."
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

def load_data(file_path=None):
    """
    Load token data from the cleaned CSV file.
    
    Args:
        file_path (str): Path to the cleaned meter data CSV
        
    Returns:
        pd.DataFrame: The loaded data
    """
    if file_path is None:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_dir, "resources", "data", "cleaned_meter_data.csv")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}. Run data_cleaning.py first.")
    
    df = pd.read_csv(file_path)
    
    # Convert Datetime column to actual datetime type if it's not already
    if 'Datetime' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['Datetime']):
        df['Datetime'] = pd.to_datetime(df['Datetime'])
    
    return df

def plot_units_over_time(df):
    """
    Plot the number of units purchased over time.
    
    Args:
        df (pd.DataFrame): The token data DataFrame
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(base_dir, "resources", "images", "units_over_time.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['Datetime'], df['Units'], marker='o', linestyle='-', color='#1f77b4')
    plt.title('Units Purchased Over Time', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Units', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved chart to: {os.path.abspath(output_path)}")
    plt.close()

def plot_amount_distribution(df):
    """
    Plot a histogram showing the distribution of purchase amounts.
    
    Args:
        df (pd.DataFrame): The token data DataFrame
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(base_dir, "resources", "images", "amount_distribution.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Amt'], bins=10, kde=True, color='#2ca02c')
    plt.title('Distribution of Purchase Amounts', fontsize=16)
    plt.xlabel('Amount (KSh)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved chart to: {os.path.abspath(output_path)}")
    plt.close()

def plot_units_per_amount(df):
    """
    Plot a scatter plot showing units received per amount spent.
    
    Args:
        df (pd.DataFrame): The token data DataFrame
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(base_dir, "resources", "images", "units_per_amount.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Amt'], df['Units'], alpha=0.7, s=50, color='#d62728')
    
    # Add trend line
    z = np.polyfit(df['Amt'], df['Units'], 1)
    p = np.poly1d(z)
    plt.plot(df['Amt'], p(df['Amt']), "r--", alpha=0.8)
    
    plt.title('Units per Amount Spent', fontsize=16)
    plt.xlabel('Amount (KSh)', fontsize=12)
    plt.ylabel('Units', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved chart to: {os.path.abspath(output_path)}")
    plt.close()

def plot_monthly_spending(df):
    """
    Plot the total monthly spending.
    
    Args:
        df (pd.DataFrame): The token data DataFrame
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(base_dir, "resources", "images", "monthly_spending.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Add month and year columns
    df['Month'] = df['Datetime'].dt.month_name()
    df['Year'] = df['Datetime'].dt.year
    
    # Group by month and year, sum the amounts
    monthly_data = df.groupby(['Year', 'Month'])['Amt'].sum().reset_index()
    
    # Create a sort key for months
    month_order = {month: i for i, month in enumerate([
        'January', 'February', 'March', 'April', 
        'May', 'June', 'July', 'August', 
        'September', 'October', 'November', 'December'
    ])}
    
    # Sort the data
    monthly_data['MonthNumber'] = monthly_data['Month'].map(month_order)
    monthly_data = monthly_data.sort_values(['Year', 'MonthNumber'])
    
    # Format x-axis labels
    x_labels = [f"{row['Month'][:3]} {row['Year']}" for _, row in monthly_data.iterrows()]
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(x_labels, monthly_data['Amt'], color='#9467bd')
    plt.title('Monthly Spending', fontsize=16)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Amount (KSh)', fontsize=12)
    plt.xticks(rotation=45)
    
    # Add value labels above bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                 f'{int(height)}',
                 ha='center', va='bottom', rotation=0)
    
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved chart to: {os.path.abspath(output_path)}")
    plt.close()

def create_comprehensive_dashboard(df):
    """
    Create a comprehensive dashboard with multiple visualizations.
    
    Args:
        df (pd.DataFrame): The token data DataFrame
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(base_dir, "resources", "images", "token_data_dashboard.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Create the figure with multiple subplots
    fig, axs = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Units over time
    axs[0, 0].plot(df['Datetime'], df['Units'], marker='o', linestyle='-', color='#1f77b4')
    axs[0, 0].set_title('Units Purchased Over Time', fontsize=14)
    axs[0, 0].set_xlabel('Date', fontsize=10)
    axs[0, 0].set_ylabel('Units', fontsize=10)
    axs[0, 0].grid(True, alpha=0.3)
    
    # 2. Distribution of purchase amounts
    sns.histplot(df['Amt'], bins=10, kde=True, ax=axs[0, 1], color='#2ca02c')
    axs[0, 1].set_title('Distribution of Purchase Amounts', fontsize=14)
    axs[0, 1].set_xlabel('Amount (KSh)', fontsize=10)
    axs[0, 1].set_ylabel('Frequency', fontsize=10)
    axs[0, 1].grid(True, alpha=0.3)
    
    # 3. Units per amount
    axs[1, 0].scatter(df['Amt'], df['Units'], alpha=0.7, s=50, color='#d62728')
    # Add trend line
    z = np.polyfit(df['Amt'], df['Units'], 1)
    p = np.poly1d(z)
    axs[1, 0].plot(df['Amt'], p(df['Amt']), "r--", alpha=0.8)
    axs[1, 0].set_title('Units per Amount Spent', fontsize=14)
    axs[1, 0].set_xlabel('Amount (KSh)', fontsize=10)
    axs[1, 0].set_ylabel('Units', fontsize=10)
    axs[1, 0].grid(True, alpha=0.3)
    
    # 4. Pie chart showing the proportion of TknAmt vs OtherCharges
    total_token_amt = df['TknAmt'].sum()
    total_other_charges = df['OtherCharges'].sum()
    
    labels = ['Token Amount', 'Other Charges']
    sizes = [total_token_amt, total_other_charges]
    explode = (0, 0.1)  # explode the 2nd slice
    
    axs[1, 1].pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90, colors=['#ff7f0e', '#8c564b'])
    axs[1, 1].set_title('Proportion of Token Amount vs Other Charges', fontsize=14)
    axs[1, 1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
      plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved comprehensive dashboard to: {os.path.abspath(output_path)}")
    plt.close()

def generate_summary_statistics(df):
    """
    Generate and print summary statistics for the token data.
    
    Args:
        df (pd.DataFrame): The token data DataFrame
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(base_dir, "resources", "data", "token_summary_statistics.txt")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Basic statistics
    stats = {
        'Total Transactions': len(df),
        'Total Amount Spent': f"KSh {df['Amt'].sum():.2f}",
        'Total Units Purchased': f"{df['Units'].sum():.2f}",
        'Average Purchase Amount': f"KSh {df['Amt'].mean():.2f}",
        'Average Units per Transaction': f"{df['Units'].mean():.2f}",
        'Average Cost per Unit': f"KSh {(df['Amt'].sum() / df['Units'].sum()):.2f}",
        'First Transaction Date': df['Datetime'].min().strftime('%Y-%m-%d'),
        'Last Transaction Date': df['Datetime'].max().strftime('%Y-%m-%d')
    }
    
    # Print summary statistics
    print("\n===== Token Data Summary Statistics =====")
    for key, value in stats.items():
        print(f"{key}: {value}")
      # Save summary statistics to a text file
    with open(output_path, 'w') as f:
        f.write("===== Token Data Summary Statistics =====\n")
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")
    
    print(f"\nSaved summary statistics to: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    try:
        print("Loading token data...")
        df = load_data()
        
        print("\nGenerating visualizations...")
        plot_units_over_time(df)
        plot_amount_distribution(df)
        plot_units_per_amount(df)
        plot_monthly_spending(df)
        create_comprehensive_dashboard(df)
        
        generate_summary_statistics(df)
        
        print("\nVisualization complete! Check the resources/images directory for generated images.")
        
    except Exception as e:
        print(f"Error: {e}")
        
        # Check if matplotlib and seaborn are installed
        try:
            import matplotlib
            import seaborn
            print("Required visualization libraries are installed.")
        except ImportError:            print("\nOne or more required libraries are not installed.")
            print("Please install them using:")
            print("pip install matplotlib seaborn pandas numpy")

def main():
    """Main function to run the visualizer."""
    try:
        print("Loading token data...")
        df = load_data()
        
        print("\nGenerating visualizations...")
        plot_units_over_time(df)
        plot_amount_distribution(df)
        plot_units_per_amount(df)
        plot_monthly_spending(df)
        create_comprehensive_dashboard(df)
        
        generate_summary_statistics(df)
        
        print("\nVisualization complete! Check the resources/images directory for generated images.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
