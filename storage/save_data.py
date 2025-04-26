from logger import get_logger
import json
import os


logger = get_logger("__name__")


def save_raw_data(weather_data: dict, filename: str) -> str:
    """
    Saves raw data received from weather api into a json file
    Args:
        weather_data (dict): data from weather api
        filename (str): filename to be saved

    Returns:
        str: not quite sure what this should be
    """
    logger.info("Started saving raw data to file")

    serialized_data = json.dumps(weather_data, indent=2)
    # TODO: Add Error Handling, permission issues, disk full etc...
    # TODO: Check to see if the file is empty or not
    if not serialized_data:
        logger.error(f"The file is empty, try again")
        raise ValueError("File empty")

    # Check if the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(serialized_data)
    except IOError as e:
        logger.error(f"Failed to write file {filename}: {e}")
        raise
    logger.info(f"Saved data to {filename}")
    return filename
