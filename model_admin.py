from model_user import User

class Admin(User):
    def __init__(self, **kwargs):
        """Initialize an admin user with inherited properties, setting user_role explicitly to 'admin'."""
        super().__init__(**kwargs)
        self.user_role = "admin"  # Ensure the user_role for admin is set to 'admin'

    def __str__(self):
        """Return string representation of an Admin object."""
        return super().__str__()

    def save(self):
        """Save the admin's information to a file."""
        with open("data/users.txt", "a") as file:
            file.write(self.__str__() + "\n")