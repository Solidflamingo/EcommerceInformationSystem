import random
import string
import time
import pandas as pd
import matplotlib.pyplot as plt
from operation_customer import CustomerOperation
from operation_product import ProductOperation
from io_interface import Interface
import os

# Aleksandar Mitreski
# ITO4133 – Introduction to Python TP2-24
# Student ID: 27565521
# operation_order.py creation date: 19/03/2024
# operation_order.py last modified date: 04/28/2024


class OrderOperation:
    ORDERS_FILE_PATH = "data/orders.txt"
    PRODUCTS_FILE_PATH = "data/products.txt"
    USERS_FILE_PATH = "data/users.txt"
    FIGURE_FOLDER = "data/figure/Customer statistics/"
    BESTSELLING_FOLDER = "data/figure/Customer statistics/Best selling data/"

    @staticmethod
    def generate_unique_order_id():
        """Generates a unique 5-digit order ID prefixed with 'o_'."""
        existing_ids = set()
        try:
            with open(OrderOperation.ORDERS_FILE_PATH, 'r') as file:
                for line in file:
                    existing_ids.add(line.split(',')[0].strip())
        except FileNotFoundError:
            Interface.print_error_message("Order Generation", "Order file not found.")
        while True:
            order_id = f"o_{random.randint(10000, 99999)}"
            if order_id not in existing_ids:
                return order_id

    @staticmethod
    def create_an_order(customer_id, product_id, create_time=None):
        """Creates a new order with a unique ID and current time if not provided."""
        # Input: customer_id (string) - ID of the customer placing the order
        #        product_id (string) - ID of the product being ordered
        #        create_time (string) - Time of order creation (optional)
        # Output: bool - True if the order is successfully created, False otherwise
        order_id = OrderOperation.generate_unique_order_id()
        create_time = create_time if create_time else time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        order_data = f"order_id:'{order_id}', user_id:'{customer_id}', pro_id:'{product_id}', order_time:'{create_time}'\n"
        try:
            with open(OrderOperation.ORDERS_FILE_PATH, 'a') as file:
                file.write(order_data)
        except IOError as e:
            Interface.print_error_message("Saving Order", f"Failed to write to file: {e}")
        return True

    @staticmethod
    def delete_order(order_id):
        """Deletes an order from the orders file based on the provided order_id."""
        # Input: order_id (string) - ID of the order to delete
        # Output: bool - True if the order is successfully deleted, False otherwise
        success = False
        try:
            with open(OrderOperation.ORDERS_FILE_PATH, 'r') as file:
                lines = file.readlines()
            with open(OrderOperation.ORDERS_FILE_PATH, 'w') as file:
                for line in lines:
                    if f"order_id:'o_{order_id}'" not in line:
                        file.write(line)
                    else:
                        success = True
        except IOError as e:
            Interface.print_error_message("Deleting Order", f"Failed to access file: {e}")
        return success

    @staticmethod
    def get_order_list(page_number=None, user_id=None):
        """Retrieves orders based on the user's role."""
        # Input: page_number (int) - Page number of orders to retrieve (optional)
        #        user_id (string) - ID of the user to retrieve orders for (optional)
        # Output: tuple - List of orders, current page number, total pages
        try:
            with open(OrderOperation.ORDERS_FILE_PATH, 'r') as file:
                orders = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            Interface.print_error_message("Order Retrieval", "Orders file not found.")
            return [], 1, 0

        # Filter orders by user_id if provided
        if user_id is not None:
            orders = [order for order in orders if f"'user_id':'{user_id}'" in order]

        items_per_page = 10
        total_orders = len(orders)
        total_pages = total_orders // items_per_page + (1 if total_orders % items_per_page else 0)

        if total_orders == 0:
            total_pages = 1

        if page_number is None:
            return orders, 1, total_pages

        start = (page_number - 1) * items_per_page
        end = start + items_per_page
        return orders[start:end], page_number, total_pages

    @staticmethod
    def parse_order(line):
        # Input: line (string) - Line from the orders file
        # Output: dict or None - Parsed order dictionary if successful, None otherwise
        try:
            order = eval(line.strip())
            return order
        except SyntaxError as e:
            Interface.print_error_message("Parsing Order", f"Error parsing order line: {e}")
            return None

    @staticmethod
    def generate_test_order_data():
        """Generates test order data for customers, saving to orders.txt and users.txt."""
        start_timestamp = int(time.time()) - (60 * 60 * 24 * 365)  # 12 months ago
        current_timestamp = int(time.time())
        try:
            products = []
            with open(OrderOperation.PRODUCTS_FILE_PATH, 'r') as file:
                for line in file:
                    product = ProductOperation.parse_product(line.strip())
                    if product:
                        products.append(product)
        except FileNotFoundError:
            Interface.print_error_message("Product Loading", "Products file not found.")
            return

        product_ids = [p['pro_id'] for p in products if 'pro_id' in p]
        customers_credentials = []  # List to store customer usernames and passwords

        for _ in range(10):
            user_name = ''.join(random.choices(string.ascii_letters + '_', k=8))
            user_password = ''.join(random.choices(string.ascii_letters, k=random.randint(1, 4))) + \
                            ''.join(random.choices(string.digits, k=1)) + \
                            ''.join(random.choices(string.ascii_letters + string.digits, k=4))
            customers_credentials.append((user_name, user_password))
            user_email = f"{user_name}@example.com"
            user_mobile = f"0{random.choice(['4', '3'])}{random.randint(10000000, 99999999)}"

            user_id = CustomerOperation.register_customer(user_name, user_password, user_email, user_mobile)
            if user_id:
                num_orders = random.randint(100, 250)  # adjusted for more meaningful data when generating figures
                for _ in range(num_orders):
                    product_id = random.choice(product_ids)
                    order_time = time.strftime("%d/%m/%y %H:%M:%S",
                                               time.localtime(random.randint(start_timestamp, current_timestamp)))
                    OrderOperation.create_an_order(user_id, product_id, order_time)
            else:
                Interface.print_message(f"Failed to register customer: {user_name}")

        Interface.print_message("\nGenerated Customer Credentials:")
        # Shows generates user_names/passwords so Admin can save original usernames and passwords for login purposes.
        for username, password in customers_credentials:
            Interface.print_message(f"Username: {username}, Password: {password}")

    @staticmethod
    def generate_single_customer_consumption_figure(customer_id):
        """Generates consumption figure for a single customer."""
        try:
            # Load product details
            products = {}
            with open(ProductOperation.PRODUCTS_FILE_PATH, 'r') as file:
                for line in file:
                    product = ProductOperation.parse_product(line)
                    if product and 'pro_id' in product:
                        products[product['pro_id']] = product

            # Load orders for the specified customer
            Interface.print_message(f"Loading orders for customer {customer_id}...")
            customer_orders = []
            with open(OrderOperation.ORDERS_FILE_PATH, 'r') as file:
                for line in file:
                    order = OrderOperation.parse_order(line)
                    if order and order['user_id'] == customer_id:
                        customer_orders.append(order)

            # Process orders for the customer
            Interface.print_message(f"Processing {len(customer_orders)} orders for customer {customer_id}...")
            order_prices = []
            for order in customer_orders:
                product = products.get(order['pro_id'])
                if product:
                    price = float(product['pro_current_price'])
                    order_time = pd.to_datetime(order['order_time'], format='%d/%m/%y %H:%M:%S')
                    order_prices.append({'order_time': order_time, 'price': price})

            # Create DataFrame from order prices
            df_orders = pd.DataFrame(order_prices)
            df_orders['month'] = df_orders['order_time'].dt.month

            # Aggregate consumption by month
            monthly_consumption = df_orders.groupby('month')['price'].sum()

            # Plotting
            plt.figure(figsize=(10, 5))
            monthly_consumption.plot(kind='bar', color='skyblue')
            plt.title(f'Monthly Consumption for Customer {customer_id}')
            plt.xlabel('Month')
            plt.ylabel('Total Consumption ($)')
            plt.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                       rotation=45)

            figure_folder = OrderOperation.FIGURE_FOLDER
            os.makedirs(figure_folder, exist_ok=True)

            figure_path = f"{figure_folder}customer_{customer_id}_consumption.png"
            plt.savefig(figure_path)
            plt.close()

        except Exception as e:
            Interface.print_error_message("Consumption Figure Generation", f"An error occurred: {e}")

    @staticmethod
    def generate_all_customers_consumption_figure():
        """Generates consumption figures for all customers."""
        try:
            # Load product details
            products = {}
            with open(ProductOperation.PRODUCTS_FILE_PATH, 'r') as file:
                for line in file:
                    product = ProductOperation.parse_product(line)
                    if product and 'pro_id' in product:
                        products[product['pro_id']] = product

            # Load all orders
            Interface.print_message("Loading all orders...")
            orders = []
            with open(OrderOperation.ORDERS_FILE_PATH, 'r') as file:
                for line in file:
                    order = OrderOperation.parse_order(line)
                    if order:
                        orders.append(order)

            # Process orders by customer
            customers = set(order['user_id'] for order in orders if 'user_id' in order)
            for customer_id in customers:
                Interface.print_message(f"Processing orders for customer {customer_id}...")
                customer_orders = [order for order in orders if order['user_id'] == customer_id]

                # Aggregate orders data for plotting
                order_prices = []
                for order in customer_orders:
                    product = products.get(order['pro_id'])
                    if product:
                        price = float(product['pro_current_price'])
                        order_time = pd.to_datetime(order['order_time'], format='%d/%m/%y %H:%M:%S')
                        order_prices.append({'order_time': order_time, 'price': price})

                # Create DataFrame from order prices
                df_orders = pd.DataFrame(order_prices)
                df_orders['month'] = df_orders['order_time'].dt.month

                # Aggregate consumption by month
                monthly_consumption = df_orders.groupby('month')['price'].sum()

                # Plotting
                plt.figure(figsize=(10, 5))
                monthly_consumption.plot(kind='bar', color='skyblue')
                plt.title(f'Monthly Consumption for Customer {customer_id}')
                plt.xlabel('Month')
                plt.ylabel('Total Consumption ($)')
                plt.xticks(range(12),
                           ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                           rotation=45)

                figure_folder = OrderOperation.FIGURE_FOLDER
                os.makedirs(figure_folder, exist_ok=True)

                figure_path = f"{figure_folder}customer_{customer_id}_consumption.png"
                plt.savefig(figure_path)
                plt.close()

        except Exception as e:
            Interface.print_error_message("Generating All Customer Consumption Figures", f"An error occurred: {e}")

    @staticmethod
    def generate_all_top_10_best_sellers_figures():
        """Generates figures for the top 10 best-selling products."""
        try:
            # Read orders data from the file
            orders = []
            with open(OrderOperation.ORDERS_FILE_PATH, 'r') as file:
                for line in file:
                    order = eval(line.strip())
                    orders.append(order)

            # Convert orders to DataFrame
            orders_df = pd.DataFrame(orders)

            # Convert order_time to datetime for easier manipulation
            orders_df['order_time'] = pd.to_datetime(orders_df['order_time'], format='%d/%m/%y %H:%M:%S')

            # Extract month from order_time
            orders_df['month'] = orders_df['order_time'].dt.month

            # Group by month and pro_id, count occurrences, and sort descending
            top_products_by_month = orders_df.groupby(['month', 'pro_id']).size().reset_index(name='order_count')
            top_products_by_month = top_products_by_month.sort_values(by=['month', 'order_count'], ascending=[True, False])

            # Define list of month names
            month_names = [
                None, 'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ]

            # Generate and save graphs for each month
            for month in range(1, 13):
                month_name = month_names[month]
                month_data = top_products_by_month[top_products_by_month['month'] == month].head(10)
                plt.figure(figsize=(10, 5))
                plt.bar(month_data['pro_id'], month_data['order_count'], color='green')
                plt.title(f'Top 10 Best Selling Products - {month_name}')
                plt.xlabel('Product ID')
                plt.ylabel('Number of Orders')
                plt.xticks(rotation=45)
                plt.tight_layout()

                # Save the graph
                figure_path = os.path.join(OrderOperation.BESTSELLING_FOLDER, f"top_10_best_sellers_{month_name.lower()}.png")
                plt.savefig(figure_path)
                plt.close()

            # Generate and save graph for the whole year
            plt.figure(figsize=(10, 5))
            year_data = top_products_by_month.groupby('pro_id')['order_count'].sum().nlargest(10)
            plt.bar(year_data.index, year_data.values, color='blue')
            plt.title('Top 10 Best Selling Products - Whole Year')
            plt.xlabel('Product ID')
            plt.ylabel('Number of Orders')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save the graph
            year_figure_path = os.path.join(OrderOperation.BESTSELLING_FOLDER, "top_10_best_sellers_year.png")
            plt.savefig(year_figure_path)
            plt.close()

        except Exception as e:
            Interface.print_error_message("Generating Top 10 Best Sellers Figures", f"An error occurred: {e}")

    @staticmethod
    def delete_all_orders():
        """Deletes all orders from the orders file."""
        open(OrderOperation.ORDERS_FILE_PATH, 'w').close()

    @staticmethod
    def delete_all_figures():
        """Recursively deletes all files in the figure folder and its subdirectories."""
        try:
            figure_folder = "data/figure/"
            for root, dirs, files in os.walk(figure_folder):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    os.remove(file_path)
        except Exception as e:
            Interface.print_error_message("Deleting All Figures", f"An error occurred: {e}")
