#!/usr/bin/env python
# -*- encoding:utf-8 -*-

__author__ = 'Adrian Wang'

import os

from disneyphoto import folder
from disneyphoto import get_temp_file_names


folder2 = 'images'


def get_downloaded_file_names():
    return [os.path.join(folder, f) for f in os.listdir(folder)]


def transform_file(input_name):
    if not os.path.exists(folder2):
        os.mkdir(folder2, 0o755)
    if not os.path.exists(input_name):
        return 0
    f = open(input_name, 'rb')
    content = f.read()
    # jpg end 0xFFD9
    end_mark = chr(0xFF) + chr(0xD9)
    pos = content.find(end_mark)
    if pos < 0:
        return 0
    output_name = input_name.replace(folder, folder2) + '.jpg'
    f_out = open(output_name, 'wb')
    f_out.write(content[pos + len(end_mark):])


# files = get_temp_file_names()
files = get_downloaded_file_names()
for f in files:
    transform_file(f)
