import pandas as pd
import sqlite3

def import_excel_data_to_db(conn, excel_file_path):
    try:
        xls = pd.ExcelFile(excel_file_path)
        cursor = conn.cursor()

        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)

            # Create table dynamically
            columns = ", ".join([f'"{col}" TEXT' for col in df.columns])
            cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS "{sheet_name}" (
                {columns}
            )
            ''')

            # Insert only new rows based on OrderID
            for index, row in df.iterrows():
                if 'OrderID' in df.columns:
                    primary_key = row['OrderID']
                    values = tuple(row)

                    # Check if record exists
                    cursor.execute(f'''
                    SELECT 1 FROM "{sheet_name}" WHERE OrderID = ?
                    ''', (primary_key,))
                    exists = cursor.fetchone()

                    if not exists:
                        placeholders = ', '.join(['?'] * len(values))
                        cursor.execute(f'''
                        INSERT INTO "{sheet_name}" ({', '.join(df.columns)})
                        VALUES ({placeholders})
                        ''', values)
                        print(f"Inserted row with OrderID: {primary_key}")
                #     else:
                #         print(f"Row with OrderID: {primary_key} already exists. Skipping.")

                # else:
                #     print("OrderID column missing in sheet. Skipping row insertion.")

            conn.commit()

        print("Excel data imported successfully.")
        return True

    except Exception as e:
        print(f"Error importing data from Excel: {e}")
        return False
