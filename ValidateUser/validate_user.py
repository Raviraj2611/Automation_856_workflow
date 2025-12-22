import sqlite3
from ErrorHandler.error_handler import User_log_error

def validate_user_credentials(conn, username_input):
    try:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT AccessLevel FROM User_Credentials WHERE username = ?
        ''', (username_input,))

        result = cursor.fetchone()

        if result:
            access_level = result[0]
            if access_level == "Full":
                return access_level
            else:
                User_log_error(username_input, "User does not have 'Full' access. AccessLevel", "DB Connection")
                print(f"User does not have 'Full' access. AccessLevel: {access_level}")
                return None
        else:
            User_log_error(username_input, "Username not found.", "DB Connection") 
            return None
    except Exception as e:
        User_log_error(username_input, "Error validating user credentials", "DB Connection")
        print(f"Error validating user credentials: {e}")
        return None
