import logging
from datetime import datetime

# Set up logging configuration
logging.basicConfig(filename='ErrorHandler/error.log', level=logging.ERROR, 
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    #Generating ErrorId
error_id = f"ERR{int(datetime.now().timestamp())}"

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def User_log_error(user_name, error_description, error_type):

    # print(user_name , error_description , error_type)

    # Log the error with the specified format
    logging.error(f"ErrorID: {error_id} | UserID: {user_name} | ErrorDescription: {error_description} | Timestamp: {timestamp}")

    print(f"Logged Error: {error_id}, Description: {error_description}, Timestamp: {timestamp}")

def log_error(order_id, error_description, error_type):

    # print(order_id , error_description , error_type)
    """
    Logs errors to a file (error.log) with the specified format:
    - ErrorID
    - OrderID (User or Order ID)
    - ErrorDescription
    - Timestamp
    """

    # Log the error with the specified format
    logging.error(f"ErrorID: {error_id} | OrderID: {order_id} | ErrorDescription: {error_description} | Timestamp: {timestamp}")

    print(f"Logged Error: {error_id}, Description: {error_description}, Timestamp: {timestamp}")


def email_error(error_description, error_type):
    logging.error(f"ErrorID: {error_id} | ErrorDescription: {error_description} | Timestamp: {timestamp}")

def db_error(error_description, error_type):
    logging.error(f"ErrorID: {error_id} | ErrorDescription: {error_description} | Timestamp: {timestamp}") 
