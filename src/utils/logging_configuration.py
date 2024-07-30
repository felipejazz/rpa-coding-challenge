import logging
from pathlib import Path

log_file_path = Path(__file__).resolve().parent.parent.parent / 'rpa-challenge.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

# Criação de um logger
logger = logging.getLogger(__name__)

