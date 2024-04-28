import random
import string
import re
from io_interface import Interface

# Aleksandar Mitreski
# ITO4133 – Introduction to Python TP2-24
# Student ID: 27565521
# creation date: 18/03/2024
# last modified date: 04/28/2024

class UserOperation:
    @staticmethod
    def generate_unique_user_id():
        """Generates a unique user ID formatted as 'u_' followed by 10 digits."""
        number = random.randint(1000000000, 9999999999)
        return f"u_{number}"

    @staticmethod
    def encrypt_password(user_password):
        """Encrypts the user password by interspersing characters from a randomly generated string."""
        chars = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(chars) for _ in range(2 * len(user_password)))
        encrypted = ''.join(r + p for r, p in zip([random_string[i:i+2] for i in range(0, len(random_string), 2)], user_password))
        return f"^^{encrypted}$$"

    @staticmethod
    def decrypt_password(encrypted_password):
        """Decrypts the previously encrypted password."""
        # Strip the '^^' at the start and the '$$' at the end
        stripped = encrypted_password[2:-2]
        # Extract every third character starting from the second character
        decrypted = ''.join(stripped[i] for i in range(2, len(stripped), 3))
        return decrypted

    @staticmethod
    def check_username_exist(user_name):
        """Checks if the username exists in 'data/users.txt'."""
        try:
            with open("data/users.txt", "r") as file:
                for line in file:
                    # Debugging output
                    # Use regular expression to match the username field in the line
                    match = re.search(fr"'user_name'\s*:\s*'({user_name})'", line)
                    if match:
                        return True
        except FileNotFoundError:
            Interface.print_error_message("Username Check", "File not found")
            return False
        return False

    @staticmethod
    def validate_username(user_name):
        """Validates that the username contains only letters, underscores, and is at least 5 characters long."""
        return len(user_name) >= 5 and all(c.isalpha() or c == '_' for c in user_name)

    @staticmethod
    def validate_password(user_password):
        """Validates password, checking it contains at least one letter, one number, and at least 5 characters long."""
        return (
            len(user_password) >= 5 and
            any(c.isalpha() for c in user_password) and
            any(c.isdigit() for c in user_password)
        )

    @staticmethod
    def login(user_name, user_password):
        """Validates the user's login credentials against the stored data."""
        try:
            with open("data/users.txt", "r") as file:
                for line in file:
                    # Manually parsing the line to create a dictionary
                    user_data = UserOperation.parse_user_data(line.strip())
                    if user_data.get('user_name') == user_name:
                        decrypted_password = UserOperation.decrypt_password(user_data.get('user_password', ''))
                        if decrypted_password == user_password:
                            # Depending on the user_role, create and return the appropriate user object
                            if user_data.get('user_role') == 'customer':
                                from model_customer import Customer
                                return Customer(**user_data), user_data.get('user_role')
                            elif user_data.get('user_role') == 'admin':
                                from model_admin import Admin
                                return Admin(**user_data), user_data.get('user_role')
            Interface.print_error_message("Login", "User not found or password incorrect.")
        except FileNotFoundError:
            Interface.print_error_message("File Access", "The user file does not exist.")
        except Exception as e:
            Interface.print_error_message("Login Error", str(e))
        return None, None

    @staticmethod
    def parse_user_data(data_str):
        """Parse a user data string into a dictionary."""
        user_data = {}
        if not data_str.strip():
            return user_data

        try:
            items = data_str.strip('{}').split(', ')
            for item in items:
                if ':' in item:
                    key, value = item.split(':', 1)  # Split only on the first colon
                    key = key.strip().strip("'")
                    value = value.strip().strip("'")
                    user_data[key] = value
                else:
                    raise ValueError(f"Item does not contain a key-value pair: {item}")
        except Exception as e:
            Interface.print_error_message("Data Parsing", f"Error parsing data: {e}")
        return user_data
