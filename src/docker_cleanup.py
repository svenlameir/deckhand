import subprocess
import logging

def prune_images(image_age: str = '24h') -> None:
    """
    Prune Docker images older than the specified age and log the output.
    Args:
        image_age (str): Age filter for images to prune (e.g., '24h').
    """
    logging.info(f"Pruning images older than {image_age}...")
    try:
        result = subprocess.run([
            'docker', 'image', 'prune', '-a', '--force', f'--filter=until={image_age}'
        ], check=True, capture_output=True, text=True)
        logging.info("Image prune completed successfully.")
        if result.stdout:
            logging.info(f"docker output:\n{result.stdout}")
        if result.stderr:
            logging.warning(f"docker error output:\n{result.stderr}")
    except FileNotFoundError:
        logging.error("Docker is not installed or not in PATH.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during prune: {e}")
        if e.stdout:
            logging.error(f"docker output:\n{e.stdout}")
        if e.stderr:
            logging.error(f"docker error output:\n{e.stderr}")