class Product:
    FILE_PATH = "data/products.txt"
    DEFAULT_PRICE = 0.00
    DEFAULT_DISCOUNT = 0
    DEFAULT_LIKES = 0

    def __init__(self, pro_id=None, pro_model=None, pro_category=None,
                 pro_name=None, pro_current_price=None, pro_raw_price=None,
                 pro_discount=None, pro_likes_count=None):
        """Initialize a product with default or specified values for its properties."""
        self.pro_id = pro_id if pro_id else self.generate_unique_pro_id()
        self.pro_model = pro_model if pro_model else "default_model"
        self.pro_category = pro_category if pro_category else "default_category"
        self.pro_name = pro_name if pro_name else "default_name"
        self.pro_current_price = float(pro_current_price) if pro_current_price else Product.DEFAULT_PRICE
        self.pro_raw_price = float(pro_raw_price) if pro_raw_price else Product.DEFAULT_PRICE
        self.pro_discount = int(pro_discount) if pro_discount else Product.DEFAULT_DISCOUNT
        self.pro_likes_count = int(pro_likes_count) if pro_likes_count else 0

    @staticmethod
    def generate_unique_pro_id():
        """Generate a unique product ID based on a seven-digit number, prefixed with 'p_'."""
        import random
        number = random.randint(1000000, 9999999)
        return f"p_{number}"

    def __str__(self):
        """Return a formatted string representation of the Product object."""
        return (f"Category: {self.pro_category}, Product Name: {self.pro_name}, "
                f"Current Price: ${self.pro_current_price:.2f}, Raw Price: ${self.pro_raw_price:.2f}, "
                f"Discount: {self.pro_discount}%, Likes Count: {self.pro_likes_count}, "
                f"ID: {self.pro_id}, Model: {self.pro_model}")

    def save(self):
        """Save the product to a file."""
        with open(Product.FILE_PATH, "a") as file:
            file.write(self.__str__() + "\n")
