# -*- coding: utf-8 -*-
import logging

from src.utils import setup_logger


def main():
    setup_logger(logging.DEBUG, r"C:\a\f.log")
    logging.debug("This is a debug message")
    logging.info("This is an info message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")
    logging.critical("This is a critical message")


if __name__ == '__main__':
    main()
