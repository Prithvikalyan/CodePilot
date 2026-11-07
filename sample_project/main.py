from database import get_users


def home():
    users = get_users()
    return {
        "message": "Welcome to Sample Project",
        "users": users
    }


if __name__ == "__main__":
    print(home())