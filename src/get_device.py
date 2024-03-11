import subprocess
import logging


def get_device():
    """
    Retrieves the device ID of the connected Android device.

    Returns:
        str: The device ID of the selected Android device.
    """
    # Execute adb command to get the list of devices
    adb_command = "adb devices"
    output = subprocess.check_output(adb_command.split()).decode().strip()

    # Parse the output to extract the device IDs
    devices = [line.split("\t")[0] for line in output.split("\n")[1:]]

# outout format:
# List of devices attached
# emulator-5554   unauthorized
# emulator-5555   device

# throw message if any of the device is unauthorized
    for line in output.split("\n")[1:]:
        if "unauthorized" in line:
            print("Unauthorized device found. Exiting...")
            logging.info("Unauthorized device found. Exiting...")
            return 'Unauthorized Device Found'

    if not devices:
        print("No devices found. Exiting...")
        logging.info("No devices found. Exiting...")
        return 'No Devices Found'

    print("\nConnected devices: ")
    logging.info("\nConnected devices: ")
    for i, device in enumerate(devices, start=1):
        print(f"{i}: {device}")
        logging.info(f"{i}: {device}")

    try:
        device_index = int(
            input(f"\nPlease enter device index (1-{len(devices)}): ")) - 1
    except ValueError:
        print("Invalid device index.")
        logging.error("Invalid device index.")
        print("Default device selected.")
        logging.info("Default device selected.")
        device = devices[0]
        return device

    if device_index < 0 or device_index >= len(devices):
        print("Invalid device index.")
        logging.error("Invalid device index.")
        print("Default device selected.")
        logging.info("Default device selected.")
        device = devices[0]
        return device

    device = devices[device_index]

    return device

# check if the device is selected or not


def check_device():
    """
    Check the status of the device.

    Returns:
        str: The status of the device. Possible values are:
            - 'Unauthorized Device Found' if an unauthorized device is found.
            - 'No Devices Found' if no devices are found.
            - The device name if a valid device is found.
    """
    device = get_device()
    if device == 'Unauthorized Device Found':
        return 'Unauthorized Device Found'
    elif device == 'No Devices Found':
        return 'No Devices Found'
    else:
        return device


def check_device_selection(device):
    """
    Checks if the device has been selected before selecting the user.

    Args:
        device (str): The current device status.

    Returns:
        bool: True if the device has been selected, False otherwise.
    """
    if device == "please check" or device == "Unauthorized Device Found" or device == "No Devices Found":
        print("Please select device first.")
        print(f"Current device (status): {device}")
        logging.warning(
            "Device not selected before selecting user or unauthorized device found.")
        input("Press Enter to continue...")
        return False
    return True
