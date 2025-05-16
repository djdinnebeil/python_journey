import logging
import os
from datetime import datetime

# Create a logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Generate log file name based on current date
log_file = f'logs/app_{datetime.now().strftime("%Y-%m-%d")}.log'

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Capture all logs >= DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# Use a named logger
logger = logging.getLogger('my_app')

def divide(a, b):
    logger.debug('Attempting to divide %s by %s', a, b)
    try:
        result = a / b
        logger.info('Division successful: %s / %s = %s', a, b, result)
        return result
    except ZeroDivisionError as e:
        logger.error('Division failed: %s', e)
        return None

def main():
    logger.info('App started')

    divide(10, 2)
    divide(5, 0)

    logger.warning('This is a warning example.')
    logger.critical('This is a critical message.')

    logger.info('App finished')

if __name__ == '__main__':
    main()
