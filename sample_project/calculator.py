def divide(a, b):
    return a / b


def get_average(numbers):
    total = sum(numbers)
    return total / len(numbers)


def find_user(users, user_id):
    for user in users:
        if user["id"] == user_id:
            return user