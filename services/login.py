class AuthenticationService:
    def __init__(self, user_services):
        self.user_services = user_services

    def authenticate_user(self, email):
        users = self.user_services.fetch_users()
        for user in users:
            if user[1] == email:
                return user
        return None

