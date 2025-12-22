import pandas as pd
from ErrorHandler.error_handler import log_error

def export_orders_to_excel(dataframe, output_file):
    missing_dc = dataframe[dataframe['DistributionCenter'].isnull()]
    missing_status = dataframe[dataframe['StatusCode'].isnull()]

    # print(dataframe)
    # Log errors for missing 'DistributionCenter'
    if not missing_dc.empty:
        for _, row in missing_dc.iterrows():
            log_error(row['OrderID'], "Missing DistributionCenter", "Missing Data")

    # Log errors for missing 'StatusCode'
    if not missing_status.empty:
        for _, row in missing_status.iterrows():
            log_error(row['OrderID'], "Missing StatusCode", "Missing Data")

#Export the order data to an Excel file with separate sheets for each DC.
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        # Group data by DistributionCenter and write each to a separate sheet
        for dc, group in dataframe.groupby('DistributionCenter'):
            group.loc[group['StatusCode'].isna(), 'ProcessingRule'] = "Missing status code"
            group[['OrderID', 'DistributionCenter','StatusCode', 'OrderDate','ProcessingRule']].to_excel(writer, sheet_name=dc, index=False)
    print(f"Processed file saved as {output_file}")
