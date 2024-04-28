import time
import random


class User:
    FILE_PATH = "data/users.txt"
    DEFAULT_ROLE = "customer"
    DEFAULT_REGISTER_TIME = "00-00-0000_00:00:00"
    ID_PREFIX = "u_"
    ID_NUM_DIGITS = 10

    def __init__(self, user_id=None, user_name=None, user_password=None,
                 user_register_time=None, user_role=None):
        """Initialize a user with a unique ID, current time, and default or specified properties."""
        self.user_id = user_id if user_id else self.generate_unique_user_id()
        self.user_name = user_name if user_name else "default_user"
        self.user_password = user_password if user_password else "default_password"
        self.user_register_time = user_register_time if user_register_time else self.DEFAULT_REGISTER_TIME
        self.user_role = user_role if user_role else self.DEFAULT_ROLE

    @staticmethod
    def current_time():
        """Return the current system time formatted for consistency."""
        return time.strftime("%d-%m-%Y_%H:%M:%SS")

    @staticmethod
    def generate_unique_user_id():
        """Generate a unique user ID based on the specified number of digits, prefixed with 'u_'."""
        number = random.randint(10**(User.ID_NUM_DIGITS-1), (10**User.ID_NUM_DIGITS)-1)
        return f"{User.ID_PREFIX}{number}"

    def __str__(self):
        """Return string representation of the User object."""
        return (f"{{'user_id':'{self.user_id}', 'user_name':'{self.user_name}', "
                f"'user_password':'{self.user_password}', 'user_register_time':'{self.user_register_time}', "
                f"'user_role':'{self.user_role}'}}")

    def save(self):
        """Save the user's information to a file."""
        with open(User.FILE_PATH, "a") as file:
            file.write(self.__str__() + "\n")
