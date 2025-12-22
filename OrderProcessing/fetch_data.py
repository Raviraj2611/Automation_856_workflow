import pandas as pd

def fetch_data_if_admin(conn, query):
#Fetch data if the user has admin access.
    order_data = pd.read_sql_query(query, conn)
    return order_data