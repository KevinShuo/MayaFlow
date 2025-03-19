# -*- coding: utf-8 -*-
import logging


def setup_logger(log_level, file_name):
    # type: (int,str) -> None
    logging.basicConfig(level=log_level,
                        format="%(asctime)s - %(levelname)s - %(pathname)s - %(funcName)s - %(message)s",
                        filename=file_name,
                        filemode="a")

    console_hander = logging.StreamHandler()
    console_hander.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(pathname)s - %(funcName)s - %(message)s")
    console_hander.setFormatter(formatter)

    logging.getLogger().addHandler(console_hander)

