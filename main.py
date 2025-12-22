from Database.db_connection import create_db_connection
from Database.import_excel import import_excel_data_to_db
from ValidateUser.validate_user import validate_user_credentials
from OrderProcessing.fetch_data import fetch_data_if_admin
from ProcessOrder.export_orders import export_orders_to_excel
from Email.sendMailOAuth import send_reports

def main():
    db_path = 'Database/automation_data.db'
    conn = create_db_connection(db_path)
    if not conn:
        return

    excel_file_path = 'Database/Automation_856_Workflow_Data.xlsx'
    if not import_excel_data_to_db(conn, excel_file_path):
        conn.close()
        return

    username_input = input("Enter your username: ")
    access_level = validate_user_credentials(conn, username_input)
    if not access_level:
        conn.close()
        return

 # Fetch order data from the database
    query = """
        SELECT 
            o.OrderID,
            o.StatusCode,
            o.DistributionCenter,
            o.OrderDate,
            r.ProcessingRule
        FROM Order_Data o
        LEFT JOIN Reference_Data r
        ON o.StatusCode = r.StatusCode
    """

    order_data = fetch_data_if_admin(conn, query)

    # Define output file path
    output_file = 'Processed_Orders_by_DC.xlsx'

    # Export the order data to an Excel file with separate sheets for each DC
    export_orders_to_excel(order_data, output_file)

    sender_email = "kaiftemp1204@gmail.com"
    send_reports(output_file,sender_email)
    
    conn.close()

if __name__ == "__main__":
    main()
