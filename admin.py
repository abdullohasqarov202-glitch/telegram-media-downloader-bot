def add_user(user_id):

    with open("users.txt","a+") as f:

        f.seek(0)

        users = f.read()

        if str(user_id) not in users:

            f.write(str(user_id) + "\n")


def get_users():

    try:

        with open("users.txt") as f:

            return f.read().splitlines()

    except:

        return []
