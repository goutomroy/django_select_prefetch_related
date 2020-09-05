import base64
import datetime
import logging
import os
import csv
import pathlib
from struct import unpack

import pandas
from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'weather_archive.bin')
        columns = []
        emp_df = pandas.read_csv(file_path, encoding='ISO-8859-1', low_memory=False)

        print(emp_df)

        # with open(file_path, "rb") as file:
        #     callable = lambda: file.read(1024)
        #     sentinel = bytes()  # or b''
        #     for chunk in iter(callable, sentinel):
        #         for byte in chunk:
        #             print(byte)

        # for byte in pathlib.Path(file_path).read_bytes():
        #     columns.append(byte)

        # d['date'] = dt.astimezone(tz=None)
        # d['temperature'] = float(row[1])
        # d['rainfall'] = float(row[2])
        # d['barometricPressure'] = float(row[3])
        # d['humidity'] = int(row[4])
        # d['windSpeed'] = int(row[5])
        # d['windDirection'] = row[6]

        # from functools import partial
        # with open(file_path, 'rb') as file:
        #     for byte in iter(partial(file.read, 13), b''):
        #         # columns.append(byte.decode("utf-8", errors="ignore"))
        #         row_format = '4peeeBBB'
        #         # buffer = unpack(row_format, byte)
        #         # columns.append(buffer)
        #         columns.append(byte)
        # logger.info(columns)
        # logger.info(type(columns[0]))
        # logger.info(f'file_path : {file_path}')
        # logger.info(f'number of rows : {len(columns)}')