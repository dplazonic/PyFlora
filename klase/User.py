class User:
    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password

    def __str__(self):
        return f"{self.first_name},{self.last_name},{self.username},{self.password}"
        #return f"First_name: {self.first_name}\nLast_name: {self.last_name}\nUsername: {self.username}"

    def get_password(self):
        return f"{self.password}"

#---- tester ---
# user = User("davor", "plazonic", "user", "admin")
# print(user)
# print(user.get_password())






