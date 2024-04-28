from io_interface import Interface
from operation_user import UserOperation
from operation_product import ProductOperation
from operation_order import OrderOperation
from operation_admin import AdminOperation
from operation_customer import CustomerOperation

# Aleksandar Mitreski
# ITO4133 – Introduction to Python TP2-24
# Student ID: 27565521
# main.py creation date: 14/03/2024
# main.py last modified date: 04/28/2024



def main():
    current_user = None
    user_role = None

    ProductOperation.extract_products_from_files() # Extract product data from CSV files and save to products.txt
    AdminOperation.register_admin() # Register the admin

    while True:
        if not current_user:
            Interface.main_menu() # Display the main menu
            choice = Interface.get_user_input("Please select an option: ", 1)[0]

            if choice == '1':  # Login
                username = Interface.get_user_input("Enter username: ", 1)[0]
                password = Interface.get_user_input("Enter password: ", 1)[0]
                current_user, user_role = UserOperation.login(username, password)
                if not current_user:
                    Interface.print_error_message("Login", "Login failed. Please check your username and password.")

            elif choice == '2':  # Register
                user_name = Interface.get_user_input("Enter username: ", 1)[0].strip()
                user_password = Interface.get_user_input("Enter password: ", 1)[0].strip()
                user_email = Interface.get_user_input("Enter email address (format: example@example.com): ", 1)[0].strip()
                user_mobile = Interface.get_user_input("Enter user mobile (must start with 04 or 03, and be 10 digits long): ", 1)[0].strip()
                if CustomerOperation.register_customer(user_name, user_password, user_email, user_mobile):
                    Interface.print_message("Registration successful!")
                else:
                    Interface.print_error_message("Registration", "Failed. Please try other credentials.")

            elif choice == '3':  # Quit
                Interface.print_message("Thank you for using our system.")
                break
            else:
                Interface.print_error_message("Menu", "Invalid option selected. Please try again.")
        else:

            if user_role == 'admin':
                Interface.admin_menu()
                choice = Interface.get_user_input("Please select an admin option: ", 1)[0]

                if choice == '1':  # Show all products with pagination
                    while True:
                        Interface.product_menu()
                        product_choice = Interface.get_user_input("Please select an option (or enter 'back' to return): ", 1)[0]
                        if product_choice.lower() == 'back':
                            break  # Return to the admin menu
                        elif product_choice == '1':  # Show all products with pagination
                            while True:
                                page_input = Interface.get_user_input("Enter page number or 'exit': ", 1)[0]
                                if page_input.isdigit():
                                    page_number = int(page_input)
                                    products, page, total_pages = ProductOperation.get_product_list(page_number)
                                    Interface.show_list('admin', 'product', (products, page, total_pages))
                                elif page_input.lower() == 'exit':
                                    break
                                else:
                                    Interface.print_error_message("Product Navigation",
                                                                  "Invalid page number. Please try again.")
                        elif product_choice == '2':  # Search by keyword
                            keyword = Interface.get_user_input("Enter the keyword to search for: ", 1)[0]
                            matched_products = ProductOperation.get_product_list_by_keyword(keyword)
                            if matched_products:
                                Interface.show_list('admin', 'product', matched_products)
                            else:
                                Interface.print_message("No products found.")
                        elif product_choice == '3':  # Search by product ID
                            product_id = Interface.get_user_input("Enter the product ID: ", 1)[0].strip()
                            product = ProductOperation.get_product_by_id(product_id)
                            if product:
                                Interface.show_list('admin', 'product', product)
                            else:
                                Interface.print_error_message("Product ID", "Product ID not found.")
                        else:
                            Interface.print_error_message("Product Menu", "Invalid option selected. Please try again.")

                elif choice == '2': # Register new customer
                    Interface.print_message("Enter customer details:")
                    user_name = Interface.get_user_input("Enter username for the new customer: ", 1)[0]
                    user_password = Interface.get_user_input("Enter password for the new customer: ", 1)[0]
                    user_email = Interface.get_user_input("Enter email address for the new customer: ", 1)[0]
                    user_mobile = Interface.get_user_input("Enter mobile number for the new customer: ", 1)[0]
                    if CustomerOperation.register_customer(user_name, user_password, user_email, user_mobile):
                        Interface.print_message("Registration successful!")
                    else:
                        Interface.print_error_message("Registration", "Failed. Please try other credentials.")

                elif choice == '3':  # View customers
                    page_number = 1
                    while True:
                        try:
                            customers, current_page, total_pages = CustomerOperation.get_customer_list(page_number)
                            if customers:
                                Interface.show_list("admin", "customer", (customers, current_page, total_pages))
                                Interface.print_message(f"Page {current_page} of {total_pages}")
                                navigation_input = input(
                                    "Enter 'next', 'prev', a specific page number, or 'exit' to return: ").strip().lower()

                                if navigation_input == 'next':
                                    if page_number < total_pages:
                                        page_number += 1
                                    else:
                                        Interface.print_message("You are on the last page.")
                                elif navigation_input == 'prev':
                                    if page_number > 1:
                                        page_number -= 1
                                    else:
                                        Interface.print_message("You are on the first page.")
                                elif navigation_input.isdigit():
                                    input_page = int(navigation_input)
                                    if 1 <= input_page <= total_pages:
                                        page_number = input_page
                                    else:
                                        Interface.print_message("Invalid page number. Please try again.")
                                elif navigation_input == 'exit':
                                    break
                                else:
                                    Interface.print_message("Invalid input. Please enter 'next', 'prev', a specific page number, or 'exit'.")
                            else:
                                Interface.print_error_message("Data issue", "No customers found on this page.")
                                break
                        except Exception as e:
                            Interface.print_error_message("Menu error", f"An error occurred: {e}")
                            break

                elif choice == '4':  # View orders
                    while True:
                        page_number = Interface.get_user_input("Enter page number or type 'return' to go back: ", 1)[0]
                        if page_number.lower() == 'return':
                            break
                        elif page_number.isdigit():
                            orders, current_page, total_pages = OrderOperation.get_order_list(int(page_number))
                            if orders:
                                Interface.show_list("admin", "order", (orders, current_page, total_pages))
                            else:
                                Interface.print_message("No orders found.")
                        else:
                            Interface.print_error_message("Input error",
                                                          "Invalid input. Please enter a page number or 'return'.")

                elif choice == '5':  # Generate test order data
                    Interface.print_message("Generating test order data...")
                    OrderOperation.generate_test_order_data()
                    Interface.print_message("Test order data generation is complete.")

                elif choice == '6':  # Generate customer consumption figures
                    try:
                        Interface.print_message("Generating consumption figures for all customers...")
                        OrderOperation.generate_all_customers_consumption_figure()
                        Interface.print_message("All customer consumption figures generated.")

                        Interface.print_message("Generating top 10 best sellers figures...")
                        OrderOperation.generate_all_top_10_best_sellers_figures()
                        Interface.print_message("Top 10 best sellers figures generated. 12 for each month, one for the whole year.")

                    except Exception as e:
                        Interface.print_error_message("data issue", f"An error occurred while generating figures: {e}")

                elif choice == '7':  # Generate figures for product data
                    try:
                        Interface.print_message("Generating product statistical figures...")
                        ProductOperation.generate_all_product_figures()
                        Interface.print_message("Product statistical figures generated.")
                    except Exception as e:
                        Interface.print_error_message("data issue", f"An error occurred while generating product statistical figures: {e}")

                elif choice == '8':  # Delete individual data
                    Interface.delete_menu()  # Display the delete menu options
                    delete_choice = Interface.get_user_input("Choose an option: ", 1)[0]

                    if delete_choice == '1':  # Delete order, input: order_id without o_
                        order_id = Interface.get_user_input("Enter the order ID to delete: ", 1)[0]
                        if OrderOperation.delete_order(order_id):
                            Interface.print_message("Order deleted successfully.")
                        else:
                            Interface.print_error_message("Delete Order",
                                                          "Failed to delete the order or order not found.")

                    elif delete_choice == '2':  # Delete customer, input: user_id without u_
                        customer_id = Interface.get_user_input("Enter the customer ID to delete: ", 1)[0]
                        if CustomerOperation.delete_customer(customer_id):
                            Interface.print_message(f"Customer {customer_id} deleted successfully.")
                        else:
                            Interface.print_error_message("Delete Customer",
                                                          "Failed to delete the customer or customer not found.")

                elif choice == '9':  # Delete all data
                    Interface.print_message(
                        "You are about to delete all data, including users, products, orders, and any information contained in the figure folder.")
                    confirm = Interface.get_user_input("Are you sure you want to proceed? (yes/no): ", 1)[0]
                    if confirm.lower() == 'yes':
                        try:
                            Interface.print_message("Deleting all data...")
                            AdminOperation.delete_all_data()
                            Interface.print_message("All data deleted.")
                        except Exception as e:
                            Interface.print_error_message("Data issue", f"An error occurred while deleting all data: {e}")
                    else:
                        Interface.print_message("Deletion process canceled.")

                elif choice == '10':  # logout
                    current_user = None
                    user_role = None
                    Interface.print_message("Logged out successfully.")
                else:
                    Interface.print_error_message("Input error", "Invalid option selected. Please try again.")

            elif user_role == 'customer':
                Interface.customer_menu()  # Display the customer menu
                choice_input = input("Please select an option: ").strip()
                if not choice_input:
                    Interface.print_error_message("Input error", "No valid option selected. Please try again.")
                    continue  # This will skip the rest of the loop and re-prompt the user
                choice_parts = choice_input.split(maxsplit=1)
                choice = choice_parts[0]

                if choice == '1':  # view current customer profile
                    Interface.print_object(current_user)

                elif choice == '2':  # Update current customer profile
                    attribute_name_input = Interface.get_user_input(
                        "Enter the attribute you want to update (user_name, user_password, user_email or user_mobile): ", 1)
                    new_value_input = Interface.get_user_input("Enter the new value: ", 1)
                    attribute_name = attribute_name_input[0]
                    new_value = new_value_input[0]

                    # Call update_profile method to update the user's profile with the new values
                    success = CustomerOperation.update_profile(attribute_name, new_value, current_user)
                    if success:
                        Interface.print_message("Profile updated successfully!")
                    else:
                        Interface.print_error_message("Profile Update",
                                                      "Failed to update profile. Please check your input.")

                elif choice == '3':  # Search products
                    if len(choice_input) > 1:  # This means a keyword was included right after '3'
                        keyword = choice_input[1]
                        matched_products = ProductOperation.get_product_list_by_keyword(keyword) # Bypass loop below to automatically search products via a keyword that followed '3'
                        if matched_products:
                            Interface.show_list('customer', 'product', matched_products)
                        else:
                            Interface.print_message("No products found.")
                    else:
                        while True:
                            Interface.product_menu()
                            product_choice = Interface.get_user_input("Please select an option (or enter 'back' to return): ", 1)[0]
                            if product_choice.lower() == 'back':
                                break  # Exit the product menu
                            elif product_choice == '1':
                                page_number = 1  # Start with the first page
                                products, page, total_pages = ProductOperation.get_product_list(
                                    page_number)  # Fetch the first page
                                Interface.show_list('customer', 'product',
                                                    (products, page, total_pages))  # Display the first page

                                while True:
                                    navigation = Interface.get_user_input("Enter 'next', 'prev', a specific page number, or 'exit':", 1)[0].lower()
                                    if navigation.isdigit():
                                        page_number = int(navigation)
                                    elif navigation == 'next':
                                        page_number = min(page_number + 1, total_pages)
                                    elif navigation == 'prev':
                                        page_number = max(page_number - 1, 1)
                                    elif navigation == 'exit':
                                        break

                                    products, page, total_pages = ProductOperation.get_product_list(
                                        page_number)  # Fetch the page after navigation
                                    Interface.show_list('customer', 'product', (products, page, total_pages))  # Display the page after navigation
                            elif product_choice == '2':
                                keyword = Interface.get_user_input("Enter the keyword to search for:", 1)[0]
                                matched_products = ProductOperation.get_product_list_by_keyword(keyword)
                                if matched_products:
                                    Interface.show_list('customer', 'product', matched_products)
                                else:
                                    Interface.print_message("No products found.")
                            elif product_choice == '3':
                                product_id = Interface.get_user_input("Enter the product ID:", 1)[0].strip()
                                product = ProductOperation.get_product_by_id(product_id)
                                if product:
                                    Interface.show_list('customer', 'product', product)
                                else:
                                    Interface.print_message("Product ID not found.")
                            else:
                                Interface.print_error_message("Product Menu",
                                                              "Invalid option selected. Please try again.")

                elif choice == '4':  # View current customer orders
                    page_number = 1
                    while True:
                        orders, current_page, total_pages = OrderOperation.get_order_list(page_number,
                                                                                          current_user.user_id)
                        Interface.print_object(f"User ID: {current_user.user_id} - Page {current_page} of {total_pages}")
                        for order in orders:
                            Interface.print_object(order)

                        # User navigation for order history pagination
                        navigation_input = input("Enter 'next', 'prev', or 'exit' to return: ").strip().lower()
                        if navigation_input == 'next':
                            if page_number < total_pages:
                                page_number += 1
                            else:
                                Interface.print_message("You are on the last page.")
                        elif navigation_input == 'prev':
                            if page_number > 1:
                                page_number -= 1
                            else:
                                Interface.print_message("You are on the first page.")
                        elif navigation_input == 'exit':
                            break
                        else:
                            Interface.print_message("Invalid input. Please enter 'next', 'prev', or 'exit'.")

                elif choice == '5':  # Generate current customer consumption figures
                    Interface.print_message(
                        f"Starting the consumption figure generation process for customer {current_user}...")
                    if current_user is not None and hasattr(current_user, 'user_id'):
                        OrderOperation.generate_single_customer_consumption_figure(current_user.user_id)
                        # Generate consumption figure for the current user
                        Interface.print_message(f"Consumption figure generated. Check the figures folder.")
                    else:
                        Interface.print_error_message("User Error", "No valid user logged in or missing user ID.")

                elif choice == '6':  # Logout
                    current_user = None
                    user_role = None
                    Interface.print_message("Logged out successfully.")
                else:
                    Interface.print_error_message("Invalid inputs", "Invalid option selected. Please try again.")


if __name__ == "__main__":
    main()
