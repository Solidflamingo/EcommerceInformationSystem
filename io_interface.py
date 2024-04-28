class Interface:

    @staticmethod
    def get_user_input(message, num_of_args):
        """
        Prompts for user input, splits it into arguments, and ensures at least the first argument is non-empty.
        Returns a list of arguments with additional empty strings if necessary to match num_of_args.
        """
        while True:
            Interface.print_message(message)
            user_input = input().split()
            if len(user_input) >= 1 and user_input[0]:
                return user_input[:num_of_args] + [''] * (num_of_args - len(user_input))
            else:
                Interface.print_error_message("Input error", "No input received, or input is not valid. Please enter a valid response.")

    @staticmethod
    def main_menu():
        """Displays options for login, registration, or exiting the application."""
        Interface.print_message("1. Login")
        Interface.print_message("2. Register")
        Interface.print_message("3. Quit")

    @staticmethod
    def admin_menu():
        """Displays administrative options related to product and user management."""
        Interface.print_message("1. Show products")
        Interface.print_message("2. Add customers")
        Interface.print_message("3. Show customers")
        Interface.print_message("4. Show orders")
        Interface.print_message("5. Generate test data")
        Interface.print_message("6. Generate all customer statistical figures")
        Interface.print_message("7. Generate all product statistical figures")
        Interface.print_message("8. Delete individual data")
        Interface.print_message("9. Delete all data")
        Interface.print_message("10. Logout")

    @staticmethod
    def customer_menu():
        """Displays options available to customers for managing their profile and viewing products."""
        Interface.print_message("1. Show profile")
        Interface.print_message("2. Update profile")
        Interface.print_message("3. Show products")
        Interface.print_message("4. Show history orders")
        Interface.print_message("5. Generate all consumption figures")
        Interface.print_message("6. Logout")

    @staticmethod
    def product_menu():
        """Displays product search options to help users find products by pagination, keyword, or ID."""
        Interface.print_message("1. Show all products (10 per page).")
        Interface.print_message("2. Search products by keyword.")
        Interface.print_message("3. Search via product ID.")

    @staticmethod
    def delete_menu():
        """Displays the delete options for individual orders and customers"""
        Interface.print_message("Select the type of data to delete:")
        Interface.print_message("1. Delete order (enter only the digits)")
        Interface.print_message("2. Delete customer (enter only the digits)")

    @staticmethod
    def show_list(user_role, list_type, object_list):
        """
        Displays a list or single item from object_list, formatted according to the user role and list type.
        Handles paginated display if object_list is a tuple with pagination details.
        """
        if isinstance(object_list, tuple):  # Handling paginated list case
            items, page_number, total_pages = object_list
            Interface.print_message(f"List of {list_type}s - Page {page_number} of {total_pages}")
            for index, item in enumerate(items, start=1):
                Interface.print_message(f"{index}. {item}")
        elif isinstance(object_list, list):  # Handling a non-paginated list of items
            for index, item in enumerate(object_list, start=1):
                Interface.print_message(f"{index}. {item}")
        else:  # Handling a single item
            Interface.print_message(f"1. {object_list}")

    @staticmethod
    def print_error_message(error_source, error_message):
        """Prints out an error message indicating the source and nature of the error."""
        print(f"Error in {error_source}: {error_message}")

    @staticmethod
    def print_message(message):
        """Prints out a given message."""
        print(message)

    @staticmethod
    def print_object(target_object):
        """Prints out an object using its string representation."""
        print(str(target_object))