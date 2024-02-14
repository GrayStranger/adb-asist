import os
import logging


def get_apk(apk_folder):
    """
    Retrieves a list of APK files from the specified folder.

    Args:
        apk_folder (str): The path to the folder containing the APK files.

    Returns:
        list: A list of selected APK files.

    Raises:
        ValueError: If the specified APK index is invalid.
    """

    # apk_folder = os.path.abspath(apk_folder)
    apk_files = [file for file in os.listdir(
        apk_folder) if file.endswith(".apk")]

    if not apk_files:
        print("No APK files found in the folder.")
        logging.info("No APK files found in the folder.")
        return

    print("\nAvailable APK files: ")
    logging.info("Available APK files:")
    # print apk files with 'select all' option
    for i, apk_file in enumerate(apk_files):
        print(f"{i+1}: {apk_file}")
        logging.info(f"{i+1}: {apk_file}")

    try:
        apk_index = int(input(
            "\nPlease enter APK index [print '999' to install all available apk's]: ")) - 1
    except ValueError:
        print("Invalid APK index. Exiting...")
        logging.error("Invalid APK index. Exiting...")
        return

    if apk_index < 0 or apk_index >= len(apk_files):
        if apk_index == 998:
            print(f"\nSelected APK: ALL apps")
            logging.info("Selected APK: ALL apps")
            return apk_files
        else:
            print("Invalid APK index. Exiting...")
            logging.error("Invalid APK index. Exiting...")
            return

    selected_apk = []
    selected_apk.append(apk_files[apk_index])
    print(f"\nSelected APK: {selected_apk}")
    logging.info(f"Selected APK: {selected_apk}")
    return selected_apk
