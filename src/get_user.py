import subprocess
import logging


def get_user():
    """
    Retrieves the user ID from the list of users on the selected device.

    Returns:
        str: The user ID chosen by the user.
    """
    # Execute adb shell command to get the list of users
    adb_command = "adb shell pm list users"
    output = subprocess.check_output(adb_command.split()).decode().strip()

    # Parse the output to extract the user IDs
    users = [user[user.index("{")+1:user.index(":")]
             for user in output.split("\n") if "{" in user and ":" in user]

    if not users:
        logging.error("No users found.")
        print("No users found.")
        exit()
    elif len(users) > 1:
        users.append("All")

    logging.info(
        "Please choose the user to install apps within selected device:")
    print("\nPlease choose the user to install apps within selected device: ")
    for i, user in enumerate(users):
        logging.info(f"{i+1}: {user}")
        print(f"{i+1}: {user}")

    user_index = input("\nPlease enter user index: ")
    try:
        user_index = int(user_index)-1
    except ValueError:
        logging.warning("Invalid user index. Using default value.")
        print("Invalid user index. Using default value.")
        user_index = len(users) - 1

    if user_index < 0 or user_index > len(users):
        logging.warning("Invalid user index. Using default value.")
        print("Invalid user index. Using default value.")
        user_index = len(users) - 1

    user = users[user_index]
    return user
