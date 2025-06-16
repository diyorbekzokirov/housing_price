import pandas as pd
import os

def create_government_support_dataframe():
    """
    Create DataFrame from government support data extracted from the image
    Data shows housing subsidies and support programs from 2002-2013
    """
    
    # Data extracted from the image
    data = {
        'Year': [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013],
        'Monthly_Supported_Households': [963, 1040, 1537, 2231, 2782, 3255, 3175, 3382, 4982, 5540, 7685, 10094],
        'Total_Annual_Subsidy_KRW_Million': [338.8, 453.4, 679.5, 976.4, 1268.2, 1497.1, 1461.6, 1992.0, 2611.5, 3102.9, 3299.0, 5562.0],
        'Annual_Subsidy_per_Household_KRW_10000': [35.2, 43.6, 44.2, 43.8, 45.6, 46.0, 46.0, 58.9, 52.4, 56.0, 42.9, 55.1]
    }
    
    # Create DataFrame
    government_support = pd.DataFrame(data)
    
    # Add calculated columns
    government_support['Total_Annual_Subsidy_KRW'] = government_support['Total_Annual_Subsidy_KRW_Million'] * 1_000_000
    government_support['Annual_Subsidy_per_Household_KRW'] = government_support['Annual_Subsidy_per_Household_KRW_10000'] * 10_000
    
    # Add growth rate calculations
    government_support['Households_Growth_Rate'] = government_support['Monthly_Supported_Households'].pct_change() * 100
    government_support['Subsidy_Growth_Rate'] = government_support['Total_Annual_Subsidy_KRW_Million'].pct_change() * 100
    
    return government_support

def save_government_support_data():
    """
    Create and save government support DataFrame to CSV
    """
    # Create DataFrame
    df = create_government_support_dataframe()
    
    # Ensure directory exists
    output_dir = '/home/unsmartboy/Documents/housing_forecast/processed_data'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to CSV
    output_path = os.path.join(output_dir, 'government_support.csv')
    df.to_csv(output_path, index=False)
    
    print(f"Government support data saved to: {output_path}")
    print(f"Data shape: {df.shape}")
    print("\nDataFrame preview:")
    print(df.head())
    
    return df

if __name__ == "__main__":
    government_support = save_government_support_data()
    
    # Display summary statistics
    print("\n" + "="*50)
    print("GOVERNMENT HOUSING SUPPORT SUMMARY (2002-2013)")
    print("="*50)
    
    print(f"Total period: {government_support['Year'].min()} - {government_support['Year'].max()}")
    print(f"Households supported (2002): {government_support.iloc[0]['Monthly_Supported_Households']:,}")
    print(f"Households supported (2013): {government_support.iloc[-1]['Monthly_Supported_Households']:,}")
    print(f"Growth in supported households: {((government_support.iloc[-1]['Monthly_Supported_Households'] / government_support.iloc[0]['Monthly_Supported_Households']) - 1) * 100:.1f}%")
    
    print(f"\nTotal subsidy (2002): ₩{government_support.iloc[0]['Total_Annual_Subsidy_KRW_Million']:.1f} million")
    print(f"Total subsidy (2013): ₩{government_support.iloc[-1]['Total_Annual_Subsidy_KRW_Million']:.1f} million")
    print(f"Growth in total subsidy: {((government_support.iloc[-1]['Total_Annual_Subsidy_KRW_Million'] / government_support.iloc[0]['Total_Annual_Subsidy_KRW_Million']) - 1) * 100:.1f}%")
    
    avg_subsidy_per_household = government_support['Annual_Subsidy_per_Household_KRW_10000'].mean()
    print(f"\nAverage subsidy per household: ₩{avg_subsidy_per_household:.1f} × 10,000 = ₩{avg_subsidy_per_household * 10000:,.0f}")
