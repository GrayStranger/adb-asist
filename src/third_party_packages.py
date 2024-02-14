import subprocess
import logging


def confirm(package):
    """
    Prompt the user to confirm the uninstallation of a package.

    Args:
        package (str): The name of the package to be uninstalled.

    Returns:
        bool: True if the user confirms the uninstallation, False otherwise.
    """
    confirm = input(
        f"Are you sure you want to uninstall package {package}? (y/n): ")
    if confirm.lower() != "y":
        print("Exiting...")
        return False
    return True


def third_party_packages(user, permission):
    """
    Lists installed third-party packages on an Android device and performs actions based on the specified permission.

    Args:
        user (str): The user ID of the Android device.
        permission (str): The permission to be granted or revoked. Possible values are 'INSTALL', 'SYSTEM_ALERT_WINDOW', or 'UNINSTALL'.

    Returns:
        None
    """
    adb_command = "adb shell pm list packages -3 -f"
    output = subprocess.check_output(adb_command.split()).decode().strip()

    package_names = [line.split("=")[-1] for line in output.split("\n")]
    package_names.append("Return to main menu")

    print("\nInstalled third-party packages: ")
    for i, package_name in enumerate(package_names, start=1):
        print(f"{i}: {package_name}")

    try:
        package = package_names[int(
            input(f"\nPlease choose the package to grant permission ({permission}): "))-1]
    except ValueError:
        print("Invalid package index. Exiting.")
        return

    if package == "Return to main menu":
        return

    if permission == 'INSTALL':
        permission_command = f"adb shell appops set --user {user} {package} REQUEST_INSTALL_PACKAGES allow"
        output = subprocess.check_output(
            permission_command.split()).decode().strip()
    elif permission == 'SYSTEM_ALERT_WINDOW':
        permission_command = f"adb shell pm grant --user {user} {package} android.permission.SYSTEM_ALERT_WINDOW"
        output = subprocess.check_output(
            permission_command.split()).decode().strip()
    elif permission == 'UNINSTALL':
        permission_command = f"adb uninstall --user {user} {package}"
        if not confirm(package):
            return
        output = subprocess.check_output(
            permission_command.split()).decode().strip()

    if "Error" in output:
        if permission == 'UNINSTALL':
            logging.error(f"Failed to uninstall package {package}.")
            logging.error(output)
            print(
                f"\033[1;31mFailed\033[0m to uninstall package {package}.")
        else:
            logging.error(f"Failed to grant permission to package {package}.")
            logging.error(output)
            print(
                f"\033[1;31mFailed\033[0m to grant permission to package {package}.")
            print(output)
    else:
        if permission == 'UNINSTALL':
            logging.info(f"Package {package} successfully uninstalled.")
            print(
                f"Package \033[1;32msuccessfully\033[0m uninstalled.")
        else:
            logging.info(f"Permission granted to package {package}.")
            print(
                f"Permission \033[1;32msuccessfully\033[0m granted to package {package}.")


def install_apk(user, apk_folder, apk_list, installed_folder):
    """
    Installs APK files on an Android device using ADB.

    Args:
        user (str): The user for whom the APKs should be installed. Use "All" to install for all users.
        apk_folder (str): The folder path where the APK files are located.
        apk_list (list): List of APK file names to be installed.
        installed_folder (str): The folder path where the installed APK files should be moved.

    Returns:
        None
    """
    if user != "All":
        command_prefix = f"adb install -g -r --user {user}"
    else:
        command_prefix = "adb install -g -r"
    for apk in apk_list:
        install_command = f"{command_prefix} \'{apk_folder}/{apk}\'"
        install_output = subprocess.check_output(
            install_command, shell=True).decode().strip()

        if "Success" in install_output:
            logging.info(f"APK {apk} installed successfully.")
            print(
                f"APK {apk}\t:\t\t - \033[1;32minstalled successfully.\033[0m")
            move_command = f"mv '{apk_folder}/{apk}' '{installed_folder}/{apk}'"
            subprocess.run(move_command, shell=True)
            print(f"APK {apk}\t:\t\t - moved to {installed_folder}")
        else:
            logging.error(f"Failed to install APK {apk}.")
            logging.error(install_output)
            print(f"Failed to install APK {apk}.")
            print(install_output)
