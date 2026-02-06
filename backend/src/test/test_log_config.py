import logging
import logging.handlers
from pathlib import Path
from module.conf.log import setup_logger, LOG_PATH

def test_log_rotation_configured():
    """Test that the logger is configured with RotatingFileHandler."""
    # Setup logger
    setup_logger()
    
    logger = logging.getLogger()
    # Find the file handler
    handler = None
    for h in logger.handlers:
        if isinstance(h, logging.handlers.RotatingFileHandler):
            # Check if it points to the correct file
            # Resolve paths to ensure they match
            if str(Path(h.baseFilename).resolve()) == str(LOG_PATH.resolve()):
                handler = h
                break
    
    assert handler is not None, "RotatingFileHandler not found for log file"
    assert handler.maxBytes == 5 * 1024 * 1024
    assert handler.backupCount == 2
