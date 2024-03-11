import os
import logging

from get_apk import get_apk
from get_device import check_device, check_device_selection
from get_user import get_user, check_user
from third_party_packages import install_apk, third_party_packages


# Configure logging
logging.basicConfig(filename='../work.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

apk_folder = "../toInstall"
installed_folder = "../installed"
device = "please check"
user = "please select before install"


def show_menu():
    """
    Displays the menu options for the APK installer tool.

    Returns:
        str: The selected option.
    """
    os.system("clear")

    logging.info("Displayed menu options")

    print(
        "\033[1;33m\nADB Automotive Software Installation Simplicity Tool (ADB-ASIST).\n\033[0m")
    print("\033[1;37mPlease select the options to proceed:\033[0m")
    print(
        f"1. Select (check) device \t(\033[1;37mcurrent device:\033[0m {device})")
    print(f"2. Select user \t\t\t(\033[1;37mcurrent user:\033[0m {user})")
    print("3. Install APK")
    print("4. Grant 'request install' permission to the app")
    print("5. Grant 'System alert' permission to the app")
    print("6. Uninstall APK")
    print("7. Exit")
    print("8. Help")

    option = input("Please enter the option: ")

    return option


apk_pack = []

while True:
    option = show_menu()

    if option == "1":
        device = check_device()
        logging.info(f"Selected device: {device}")
        print(f"Selected device: {device}")
        input("Press Enter to continue...")
    elif option == "2":
        # check if the device is selected and authorized
        if not check_device_selection(device):
            continue
        user = get_user()
        logging.info(f"Selected user: {user}")
        print(f"Selected user: {user}")
        input("Press Enter to continue...")
    elif option == "3":
        if not check_user(user):
            continue
        apk_pack = get_apk(apk_folder)
        if apk_pack is not None:
            install_apk(user, apk_folder, apk_pack, installed_folder)
            logging.info("APK installed successfully")
        input("Press Enter to continue...")
    elif option == "4":
        if not check_user():
            continue
        third_party_packages(user, permission='INSTALL')
        logging.info("Granted 'request install' permission to the app")
        input("Press Enter to continue...")
    elif option == "5":
        if not check_user():
            continue
        third_party_packages(user, permission='SYSTEM_ALERT_WINDOW')
        logging.info("Granted 'System alert' permission to the app")
        input("Press Enter to continue...")
    elif option == "6":
        if not check_user():
            continue
        third_party_packages(user, permission='UNINSTALL')
        logging.info("Uninstalled APK")
        input("Press Enter to continue...")
    elif option == "7":
        logging.info("Exiting the APK installer tool")
        exit()
    elif option == "8":
        logging.info("Displayed help")
        # print README.md
        with open("../README.md", "r") as file:
            print(file.read())
        input("Press Enter to continue...")
    else:
        logging.warning("Invalid option selected")
        print("Invalid option. Try again.\n")
        input("Press Enter to continue...")
