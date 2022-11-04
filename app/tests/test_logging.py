from logging import NullHandler
from logging.handlers import RotatingFileHandler
from unittest import TestCase
from app.logging import get_logger


class TestLogging(TestCase):
    def test_get_logger_without_file(self):
        logger = get_logger('without')
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], NullHandler)

    def test_get_logger_with_file(self):
        logger = get_logger('with', 'test.log')
        handlers = logger.handlers
        handler = next(
            (h for h in handlers if isinstance(h, RotatingFileHandler)), None)
        self.assertIsInstance(handler, RotatingFileHandler)
