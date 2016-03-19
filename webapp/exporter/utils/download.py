#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import boto3

from django.conf import settings

from .export import FILENAMES

AWS_S3_KEY = settings.AWS_S3['access_key']
AWS_S3_SECRET = settings.AWS_S3['secret_access_key']
AWS_BUCKET = settings.AWS_S3['bucket']


def download(s3_files, path, export_aux=True, filenames=FILENAMES):
    s3 = boto3.client('s3', aws_access_key_id=AWS_S3_KEY, aws_secret_access_key=AWS_S3_SECRET)

    with open(os.path.join(path, filenames['worduse_data']), 'wb') as f:
        for file in s3_files['worduse_qs']:
            f.write(file.get_file().read())

    with open(os.path.join(path, filenames['wordcoarse_data']), 'wb') as f:
        for file in s3_files['coarse_qs']:
            f.write(file.get_file().read())

    with open(os.path.join(path, filenames['informers_data']), 'wb') as f:
        f.write(s3_files['informer'].get_file().read())

    with open(os.path.join(path, filenames['meanings_data']), 'wb') as f:
        f.write(s3_files['meaning'].get_file().read())