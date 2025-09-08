from docker_cleanup import prune_images
from utils import get_env_variable, parse_interval, set_timezone_from_env
import logging
import time

def main() -> None:
    """
    Main loop to periodically prune Docker images.
    """
    # Set timezone from environment variable
    set_timezone_from_env()
    # Configure logging format and level
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Get image age and run interval from environment variables
    image_age = get_env_variable('IMAGE_AGE', '24h')
    run_interval_str = get_env_variable('RUN_INTERVAL', '3600')
    try:
        run_interval = parse_interval(run_interval_str)
    except ValueError:
        # Handle invalid interval value
        logging.warning(f"Invalid RUN_INTERVAL '{run_interval_str}', using default 3600 seconds.")
        run_interval = 3600

    # Main loop: prune images and sleep for the interval
    while True:
        prune_images(image_age)
        logging.info(f"Sleeping for {run_interval} seconds...\n")
        time.sleep(run_interval)

if __name__ == "__main__":
    main()