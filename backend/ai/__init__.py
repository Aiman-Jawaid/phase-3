import logging

# Configure logging for AI components
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handler and formatter
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

# Add handler to logger
if not logger.handlers:
    logger.addHandler(handler)

__version__ = "0.1.0"
__author__ = "AI Todo Chatbot"