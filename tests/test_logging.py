# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(pathname)s - %(funcName)s - %(message)s",
                    filename="a.log", filemode="a")


# 记录日志
def test_loging_module():
    logging.debug("This is a debug message")
    logging.info("This is an info message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")
    logging.critical("This is a critical message")


test_loging_module()

print("Logs are written to app.log.")
