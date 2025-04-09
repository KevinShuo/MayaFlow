# -*- coding: utf-8 -*-
import os
import re

a = r"D:\longhaisi"
start_path =
for root, dirs, files in os.walk(a):
    for filename in files:
        full_path = os.path.join(root, filename).replace('\\', '/')
        if filename.endswith('.ass'):
            with open(full_path, 'r', encoding='utf-8') as f:
                data = f.read()
                for chunk in re.findall(r"filename \"(.*?)\"", data, re.DOTALL):
                    print(chunk)
            break
