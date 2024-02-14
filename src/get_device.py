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
