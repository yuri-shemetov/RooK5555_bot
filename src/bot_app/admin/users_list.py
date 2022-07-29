def get_registered_users():
    with open("bot_app/admin/settings/registered_users.txt", "r") as registered_users:
        return registered_users.read()


def get_ban_users():
    with open("bot_app/admin/settings/ban_users.txt", "r") as registered_users:
        return registered_users.read()
