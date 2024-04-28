from model_user import User

class Customer(User):
    def __init__(self, user_email=None, user_mobile=None, **kwargs):
        """Initialize a customer with default or provided email and mobile, in addition to inherited properties."""
        super().__init__(**kwargs)
        self.user_email = user_email if user_email else "default_email@example.com"
        self.user_mobile = user_mobile if user_mobile else "default_mobile"

    def __str__(self):
        """Return string representation of a Customer object, adding email and mobile information."""
        parent_str = super().__str__()[:-1]  # Get the User string representation and strip the closing brace
        return (f"{parent_str}, 'user_email':'{self.user_email}', 'user_mobile':'{self.user_mobile}'}}")

    def save(self):
        """Save the customer's information to a file."""
        with open("data/users.txt", "a") as file:
            file.write(self.__str__() + "\n")

