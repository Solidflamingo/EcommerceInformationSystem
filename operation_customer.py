import re
import time
from model_customer import Customer
from operation_user import UserOperation
from io_interface import Interface

# Aleksandar Mitreski
# ITO4133 – Introduction to Python TP2-24
# Student ID: 27565521
# creation date: 14/03/2024
# last modified date: 04/28/2024

class CustomerOperation:
    @staticmethod
    def validate_email(user_email):
        """Validate the email address format."""
        # Input: user_email (string) - Email address to validate
        # Output: bool - True if the email is in a valid format, False otherwise
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(pattern, user_email))

    @staticmethod
    def validate_mobile(user_mobile):
        """Validate the mobile number format."""
        # Input: user_mobile (string) - Mobile number to validate
        # Output: bool - True if the mobile number is in a valid format, False otherwise
        return bool(re.match(r'^(04|03)\d{8}$', user_mobile))

    @staticmethod
    def register_customer(user_name, user_password, user_email, user_mobile):
        """Register a new customer with validated details and encrypted password."""
        # Input: user_name (string) - Customer's username
        #        user_password (string) - Customer's password
        #        user_email (string) - Customer's email address
        #        user_mobile (string) - Customer's mobile number
        # Output: string or False - Generated user ID if registration is successful, False otherwise
        if UserOperation.check_username_exist(user_name):
            Interface.print_message(f"Username already exists: {user_name}")
            return False
        if not CustomerOperation.validate_email(user_email):
            Interface.print_message(f"Invalid email: {user_email}")
            return False
        if not CustomerOperation.validate_mobile(user_mobile):
            Interface.print_message(f"Invalid mobile: {user_mobile}")
            return False
        if not UserOperation.validate_username(user_name):
            Interface.print_message(f"Invalid username: {user_name}")
            return False
        if not UserOperation.validate_password(user_password):
            Interface.print_message(f"Invalid password for {user_name}")
            return False

        user_id = UserOperation.generate_unique_user_id()

        encrypted_password = UserOperation.encrypt_password(user_password)

        # Record the registration time
        registration_time = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())

        # Create the customer object
        customer = Customer(
            user_id=user_id,  # Use the generated user ID
            user_name=user_name,
            user_password=encrypted_password,
            user_email=user_email,
            user_mobile=user_mobile,
            user_register_time=registration_time
        )

        customer.save()
        return user_id

    @staticmethod
    def update_profile(attribute_name, value, customer_object):
        """Update customer profile after validating input values."""
        # Input: attribute_name (string) - Name of the attribute to update
        #        value (string) - New value for the attribute
        #        customer_object (Customer) - Instance of the Customer class to update
        # Output: bool - True if the profile is successfully updated, False otherwise
        valid = False
        users = []
        try:
            with open("data/users.txt", "r") as file:
                users = file.readlines()
        except Exception as e:
            Interface.print_error_message("Opening users file", f"Error reading users file: {e}")
            return False

        if attribute_name == "user_email":
            valid = CustomerOperation.validate_email(value)
        elif attribute_name == "user_mobile":
            valid = CustomerOperation.validate_mobile(value)
        elif attribute_name == "user_name":
            valid = UserOperation.validate_username(value)
            if valid:  # Only proceed to check existing usernames if the new username is valid
                username_exists = any(
                    f"'user_name':'{value}'" in user_line and f"'user_id':'{customer_object.user_id}'" not in user_line
                    for user_line in users)
                if username_exists:
                    Interface.print_message("Username already exists.")
                    valid = False  # Invalidate the operation if the username exists
        elif attribute_name == "user_password":
            valid = True

        if valid:
            if attribute_name == "user_password":
                value = UserOperation.encrypt_password(value)  # Encrypt the password before updating
            setattr(customer_object, attribute_name, value)
            # Rewrite the user details in the file
            try:
                updated = False
                with open("data/users.txt", "w") as file:
                    for user_line in users:
                        if f"'user_id':'{customer_object.user_id}'" in user_line:
                            # Update the user line with new information
                            file.write(str(customer_object) + "\n")
                            updated = True
                        else:
                            file.write(user_line)
                return updated
            except Exception as e:
                Interface.print_error_message("Updating Profile", f"Error updating profile: {e}")
                return False
        else:
            return False

    @staticmethod
    def delete_customer(customer_id):
        """Delete a customer based on the customer_id."""
        # Input: customer_id (string) - ID of the customer to delete
        # Output: bool - True if the customer is successfully deleted, False otherwise
        updated_lines = []
        deleted = False
        try:
            with open("data/users.txt", "r") as file:
                lines = file.readlines()

            for line in lines:
                if f"'user_id':'u_{customer_id}'" not in line:
                    updated_lines.append(line)
                else:
                    deleted = True

            with open("data/users.txt", "w") as file:
                file.writelines(updated_lines)

        except Exception as e:
            Interface.print_error_message("Data issue", f"An error occurred: {e}")

        return deleted

    @staticmethod
    def get_customer_list(page_number):
        """Retrieve a list of customers per page from the data file."""
        # Input: page_number (int) - Page number to retrieve
        # Output: tuple - List of Customer objects, current page number, total pages
        try:
            with open("data/users.txt", "r") as file:
                lines = file.readlines()
            customers_per_page = 10
            total_pages = len(lines) // customers_per_page + (1 if len(lines) % customers_per_page else 0)
            start = (page_number - 1) * customers_per_page
            end = min(start + customers_per_page, len(lines))

            customers = []
            for line in lines[start:end]:
                try:
                    entries = line.strip().strip('{}').split(", ")
                    customer_dict = {}
                    for entry in entries:
                        parts = entry.split(':', 1)
                        if len(parts) == 2:
                            key, value = parts
                            customer_dict[key.strip("'")] = value.strip("'")
                    if customer_dict:
                        customers.append(Customer(**customer_dict))
                except ValueError:
                    Interface.print_message(f"Skipping malformed line: {line}")

            return customers, page_number, total_pages
        except Exception as e:
            Interface.print_error_message("Customer list", f"Failed to retrieve customer list: {e}")
            return [], page_number, 0

    @staticmethod
    def delete_all_customers():
        """Remove all customers and admins from the data file."""
        try:
            with open("data/users.txt", "w") as file:
                pass
        except Exception as e:
            Interface.print_error_message("Deleting All Users", f"An error occurred while deleting all users: {e}")

