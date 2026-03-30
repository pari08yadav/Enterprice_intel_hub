import logging

# 1. Configure the logger
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 2. Create a logger object
logger = logging.getLogger(__name__)

