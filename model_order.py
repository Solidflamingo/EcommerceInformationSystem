import time
import random
from io_interface import Interface
class Order:
    FILE_PATH = "data/orders.txt"
    ID_PREFIX = "o_"
    ID_NUM_DIGITS = 5

    def __init__(self, order_id=None, user_id=None, pro_id=None, order_time=None):
        """Initialize an order with unique ID and order time."""
        self.order_id = order_id if order_id else self.generate_unique_order_id()
        self.user_id = user_id
        self.pro_id = pro_id
        self.order_time = order_time if order_time else Order.current_time()

    @staticmethod
    def current_time():
        """Return the current system time formatted for consistency."""
        return time.strftime("%d-%m-%Y_%H:%M:%SS")

    @staticmethod
    def generate_unique_order_id():
        """Generate a unique order ID based on the specified number of digits, prefixed appropriately."""
        number = random.randint(10**(Order.ID_NUM_DIGITS-1), (10**Order.ID_NUM_DIGITS)-1)
        return f"{Order.ID_PREFIX}{number}"

    def __str__(self):
        """Return string representation of the Order object."""
        return (f"{{'order_id':'{self.order_id}', 'user_id':'{self.user_id}', 'pro_id':'{self.pro_id}', "
                f"'order_time':'{self.order_time}'}}")

    def save(self):
        """Save the order to a file, handling any exceptions during the process."""
        try:
            with open(Order.FILE_PATH, "a") as file:
                file.write(self.__str__() + "\n")
        except Exception as e:
            Interface.print_error_message("Save error", f"Error when saving order: {e}")  # Catch any errors
