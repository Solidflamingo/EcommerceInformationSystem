from model_admin import Admin
from datetime import datetime
from operation_user import UserOperation
from operation_order import OrderOperation
from operation_customer import CustomerOperation
from operation_product import ProductOperation
from io_interface import Interface


# Aleksandar Mitreski
# ITO4133 – Introduction to Python TP2-24
# Student ID: 27565521
# creation date: 12/03/2024
# last modified date: 04/28/2024

class AdminOperation:
    USERS_FILE_PATH = "data/users.txt"
    DEFAULT_ADMIN_USERNAME = "SystemAdmin"
    DEFAULT_ADMIN_PASSWORD = "AdminSecure123"

    @staticmethod
    def register_admin():
        """Register an admin account if it does not already exist, to be called at system startup."""
        # Check if admin username already exists
        if not UserOperation.check_username_exist(AdminOperation.DEFAULT_ADMIN_USERNAME):
            # Generate unique user ID
            user_id = UserOperation.generate_unique_user_id()

            # Use the default admin password directly
            encrypted_password = UserOperation.encrypt_password(AdminOperation.DEFAULT_ADMIN_PASSWORD)

            registration_time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

            # Create and save the new admin
            admin = Admin(user_id=user_id, user_name=AdminOperation.DEFAULT_ADMIN_USERNAME,
                          user_password=encrypted_password, user_register_time=registration_time, user_role='admin')
            admin.save()
        else:
            pass


    @staticmethod
    def delete_all_data():
        """Deletes all data including orders, customers, products, and figures."""
        try:
            # Delete all orders
            OrderOperation.delete_all_orders()

            # Delete all customers
            CustomerOperation.delete_all_customers()

            # Delete all products
            ProductOperation.delete_all_products()

            # Delete all figures generated
            OrderOperation.delete_all_figures()

        except Exception as e:
            Interface.print_message(f"An error occurred while deleting all data: {e}")
