# -*- coding: utf-8 -*-
import importlib

from check_and_publish.src.view import publish

importlib.reload(publish)
if __name__ == '__main__':
    check_view = publish.PublishView()
