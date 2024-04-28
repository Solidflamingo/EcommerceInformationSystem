import csv
import os
import matplotlib.pyplot as plt
import re
from io_interface import Interface


class ProductOperation:
    PRODUCTS_FILE_PATH = "data/products.txt"
    SOURCE_FOLDER = "data/product/"
    FIGURE_FOLDER = "data/figure/Product statistics/"

    @staticmethod
    def extract_products_from_files():
        """Extracts product data from CSV files and saves it to a TXT file."""
        # Mapping of Excel column names to the corresponding keys with 'pro_' prefix
        column_name_mapping = {
            'id': 'pro_id',
            'model': 'pro_model',
            'category': 'pro_category',
            'name': 'pro_name',
            'current_price': 'pro_current_price',
            'raw_price': 'pro_raw_price',
            'discount': 'pro_discount',
            'likes_count': 'pro_likes_count'
        }
        products = []
        # Iterate through each CSV file in the source folder
        for filename in os.listdir(ProductOperation.SOURCE_FOLDER):
            if filename.endswith('.csv'):
                with open(ProductOperation.SOURCE_FOLDER + filename, mode='r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Extract required fields and convert column names
                        product_data = {column_name_mapping[column]: value for column, value in row.items() if column in column_name_mapping}
                        products.append(product_data)
        with open(ProductOperation.PRODUCTS_FILE_PATH, 'w', encoding='utf-8') as file:
            for product in products:
                file.write(str(product) + '\n')

    @staticmethod
    def get_product_list(page_number):
        """Retrieves a paginated list of products from the products file."""
        try:
            with open(ProductOperation.PRODUCTS_FILE_PATH, 'r') as file:
                lines = file.readlines()
            products_per_page = 10
            total_pages = (len(lines) // products_per_page) + (1 if len(lines) % products_per_page else 0)
            start_index = (page_number - 1) * products_per_page
            end_index = min(start_index + products_per_page, len(lines))
            page_products = [eval(line.strip()) for line in lines[start_index:end_index]]
            return (page_products, page_number, total_pages)
        except FileNotFoundError:
            Interface.print_error_message("Product List Retrieval", "Product file not found.")
            return ([], page_number, 0)
        except Exception as e:
            Interface.print_error_message("Product List Retrieval", f"An error occurred: {e}")
            return ([], page_number, 0)

    @staticmethod
    def get_product_by_id(product_id):
        """Retrieves a single product by its ID."""
        try:
            product_id = str(product_id).strip()  # Convert to string and strip any extraneous whitespace
            with open(ProductOperation.PRODUCTS_FILE_PATH, 'r') as file:
                for line in file:
                    line = line.strip()  # Remove any leading/trailing whitespace from the line
                    if not line:
                        continue
                    product = eval(line)  # Convert the line to a dictionary
                    if 'pro_id' in product and str(product['pro_id']).strip() == product_id:
                        return product
            Interface.print_error_message("Product Retrieval", "Product ID not found.")
        except FileNotFoundError:
            Interface.print_error_message("Product Retrieval", "Product file not found.")
        except SyntaxError as e:
            Interface.print_error_message("Product Retrieval", "Syntax error.")
        except Exception as e:
            Interface.print_error_message("Product Retrieval", "Product ID not found.")
        return None

    @staticmethod
    def get_product_list_by_keyword(keyword):
        """Finds products by keyword in product names."""
        matched_products = []
        with open(ProductOperation.PRODUCTS_FILE_PATH, 'r') as file:
            for line in file:
                if keyword.lower() in line.lower():
                    matched_products.append(eval(line))
        return matched_products

    @staticmethod
    def parse_product(line):
        """Parses a product data line into a dictionary."""
        product = {}
        line = line.strip('{}\n')
        pairs = re.findall(r"\'([\w_]+)\':\s*\'([^\']+?)\'", line)
        for key, value in pairs:
            product[key] = value
        return product

    @staticmethod
    def generate_category_figure():
        """Generates a bar chart of products by category."""
        categories = {}
        with open(ProductOperation.PRODUCTS_FILE_PATH, 'r') as file:
            for line in file:
                product = eval(line)
                category = product['pro_category']
                categories[category] = categories.get(category, 0) + 1
        # Plotting
        categories_sorted = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        fig, ax = plt.subplots()
        ax.bar([x[0] for x in categories_sorted], [x[1] for x in categories_sorted])
        ax.set_xlabel('Category')
        ax.set_ylabel('Number of Products')
        ax.set_title('Total Products by Category')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(ProductOperation.FIGURE_FOLDER, 'generate_category_figure.png'))
        plt.close()

    @staticmethod
    def generate_discount_figure():
        """Generates a pie chart showing the proportion of discounts."""
        discount_ranges = {'<30': 0, '30-60': 0, '>60': 0}
        with open(ProductOperation.PRODUCTS_FILE_PATH, 'r') as file:
            for line in file:
                product = eval(line)
                discount = float(product['pro_discount'])
                if discount < 30:
                    discount_ranges['<30'] += 1
                elif 30 <= discount <= 60:
                    discount_ranges['30-60'] += 1
                else:
                    discount_ranges['>60'] += 1

        # Plotting
        fig, ax = plt.subplots()
        ax.pie(discount_ranges.values(), labels=[f"<30%", "30-60%", ">60%"], autopct='%1.1f%%')
        ax.set_title('Product Discounts')

        figure_folder = os.path.join(ProductOperation.FIGURE_FOLDER, 'generate_discount_figure.png')
        if not os.path.exists(os.path.dirname(figure_folder)):
            os.makedirs(os.path.dirname(figure_folder))

        plt.savefig(figure_folder)
        plt.close()

    @staticmethod
    def generate_likes_count_figure():
        """Generates a chart displaying the sum of likes counts for each category."""
        likes_counts = {}
        with open(ProductOperation.PRODUCTS_FILE_PATH, 'r') as file:
            for line in file:
                product = eval(line)
                category = product['pro_category']
                likes_counts[category] = likes_counts.get(category, 0) + int(product['pro_likes_count'])

        # Sorting the categories by their total likes count in ascending order
        sorted_likes_counts = sorted(likes_counts.items(), key=lambda x: x[1])

        # Plotting
        fig, ax = plt.subplots()
        ax.barh([category for category, _ in sorted_likes_counts],
                [likes_count for _, likes_count in sorted_likes_counts])
        ax.set_xlabel('Total Likes (Millions)')
        ax.set_title('Total Likes Count by Category')

        # Format x-axis to show full numbers without scientific notation
        ax.set_xticks([0, 1e6, 2e6, 3e6, 4e6])
        ax.set_xticklabels(['0', '1M', '2M', '3M', '4M'])

        plt.tight_layout()

        figure_folder = os.path.join(ProductOperation.FIGURE_FOLDER, 'total_likes_count_by_category.png')
        if not os.path.exists(os.path.dirname(figure_folder)):
            os.makedirs(os.path.dirname(figure_folder))

        plt.savefig(figure_folder)
        plt.close()

    @staticmethod
    def generate_discount_likes_count_figure():
        """Generates a scatter chart showing the relationship between likes count and discount."""
        discounts = []
        likes_counts = []
        with open(ProductOperation.PRODUCTS_FILE_PATH, 'r') as file:
            for line in file:
                product = eval(line)
                discounts.append(float(product['pro_discount']))
                likes_counts.append(int(product['pro_likes_count']))
        # Plotting
        plt.scatter(likes_counts, discounts)
        plt.xlabel('Likes Count')
        plt.ylabel('Discount (%)')
        plt.title('Relationship between Likes Count and Discount')
        plt.savefig(os.path.join(ProductOperation.FIGURE_FOLDER, 'generate_discount_likes_count_figure.png'))
        plt.close()

    @staticmethod
    def generate_all_product_figures():
        """Generates all product statistical figures."""
        ProductOperation.generate_category_figure()
        ProductOperation.generate_discount_figure()
        ProductOperation.generate_likes_count_figure()
        ProductOperation.generate_discount_likes_count_figure()

    @staticmethod
    def delete_all_products():
        """Removes all product data from the products file."""
        open(ProductOperation.PRODUCTS_FILE_PATH, 'w').close()

