# -*- coding: utf-8 -*-
import importlib

from check_and_publish.src.view import check

importlib.reload(check)
if __name__ == '__main__':
    check_view = check.CheckView()
    check_view.run()
