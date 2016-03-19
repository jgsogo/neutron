#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import boto3

from botocore.exceptions import ClientError
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.dateparse import parse_datetime
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.timezone import datetime, timedelta, now
from django.db import IntegrityError, transaction

from neutron.models import WordUse, CoarseWord

from .utils.export import export
from .utils.tempdir import tempdir

AWS_S3_KEY = settings.AWS_S3['access_key']
AWS_S3_SECRET = settings.AWS_S3['secret_access_key']
AWS_BUCKET = settings.AWS_S3['bucket']

import logging
log = logging.getLogger(__name__)

s3 = boto3.client('s3', aws_access_key_id=AWS_S3_KEY, aws_secret_access_key=AWS_S3_SECRET)


class AWSObject(models.Model):
    bucket = models.CharField(max_length=64)
    key = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(AWSObject, self).__init__(*args, **kwargs)
        self.bucket = AWS_BUCKET

    def save(self, key=None, *args, **kwargs):
        if not self.key and key:
            self.key = key
        super(AWSObject, self).save(*args, **kwargs)

    def exists(self):
        try:
            s3.head_object(Bucket=self.bucket, Key=self.key)
            return True
        except ClientError:
            return False

    def get_file(self):
        try:
            r = s3.get_object(Bucket=self.bucket, Key=self.key)
            return r['Body']
        except ClientError:
            return None

    def save_from_file(self, filename):
        s3.upload_file(Bucket=self.bucket, Key=self.key, Filename=filename)

    def save_from_text(self, content):
        s3.put_object(Bucket=self.bucket, Key=self.key, Body=content.encode())


class ExportIndexManager(models.Manager):
    def incremental_dump(self, name, user=None, version=None):
        log.info("Requested incremental dump for '{name}' (version='{version}')".format(name=name, version=version))
        try:
            index = self.get(name=name)
        except self.model.DoesNotExist:
            index = self.model.objects.create(name=name, user=None)
        return index.incremental_dump(version)


@python_2_unicode_compatible
class ExportIndex(AWSObject):
    MINIMUM_PERIOD = timedelta(hours=1)

    name = models.CharField(unique=True, max_length=64, help_text=_('This will be the folder inside Amazon S3 bucket'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, help_text=_('Who ordered this export (blank for system)'))
    last_date = models.DateTimeField(blank=True, null=True)

    objects = ExportIndexManager()

    class Meta:
        abstract = False

    def save(self, content=None, *args, **kwargs):
        if not self.key:
            self.key = slugify(self.name) + '.txt'
        super(ExportIndex, self).save(*args, **kwargs)
        if content:
            self.save_from_text(content)

    def __str__(self):
        return self.name

    def incremental_dump(self, version):
        time_now = now()

        if self.last_date and self.last_date + ExportIndex.MINIMUM_PERIOD > time_now:
            log.warn("Abort incremental dump. Cannot perform another one until {}".format(self.last_date + ExportIndex.MINIMUM_PERIOD))
            return False

        # Gather data
        worduse_data = WordUse.objects.all()
        coarse_data = CoarseWord.objects.all()

        f = self.get_file()
        lines = []
        last_date = None
        if f:
            lines = f.read().decode().split('\n')
            last_date = parse_datetime(lines[0])
            worduse_data = worduse_data.filter(timestamp__range=(last_date, time_now))
            coarse_data = coarse_data.filter(timestamp__range=(last_date, time_now))
            log.debug(" - dump between: '{start}' and '{end}'".format(start=last_date, end=time_now))
        else:
            log.debug(" - dump between: -- and '{end}'".format(end=time_now))

        # Store temp files:
        with tempdir() as dirpath:
            log.debug(" - exporting data to '{dirpath}'".format(dirpath=dirpath))
            filenames = export(worduse_data, coarse_data, dirpath, export_aux=False)

            with transaction.atomic():
                log.debug(" - save worduse_data")
                worduse = IncrementalFile(index=self, name='worduse', version=version, start=last_date, end=time_now)
                worduse.save(file=os.path.join(dirpath, filenames['worduse_data']))

                log.debug(" - save coarse_data")
                wordcoarse = IncrementalFile(index=self, name='coarse', version=version, start=last_date, end=time_now)
                wordcoarse.save(file=os.path.join(dirpath, filenames['wordcoarse_data']))

                log.debug(" - save informer_data")
                informers = OverrideFile(index=self, name='informer', version=version, end=time_now)
                informers.save(file=os.path.join(dirpath, filenames['informers_data']))

                log.debug(" - save meaning_data")
                meanings = OverrideFile(index=self, name='meaning', version=version, end=time_now)
                meanings.save(file=os.path.join(dirpath, filenames['meanings_data']))

                log.debug(" - update export_index")
                lines.insert(0, time_now.strftime('%Y-%m-%d-%H-%M-%S'))
                self.last_date = time_now
                self.save(content='\n'.join(lines))
        return True

    def get_data(self, version, from_date=None, to_date=None):
        filters = {}
        if to_date:
            filters.update({'end__lte': to_date})

        worduse = IncrementalFile.objects.filter(index=self, version=version, name='worduse').filter(**filters)
        coarse = IncrementalFile.objects.filter(index=self, version=version, name='coarse').filter(**filters)
        informer = OverrideFile.objects.filter(index=self, version=version, name='informer').filter(**filters)
        meaning = OverrideFile.objects.filter(index=self, version=version, name='meaning').filter(**filters)

        if from_date:
            worduse = worduse.filter(start__gte=from_date)
            coarse = coarse.filter(start__gte=from_date)

        return {'worduse': [(it.bucket, it.key) for it in worduse],
                'coarse': [(it.bucket, it.key) for it in coarse],
                'informer': [(it.bucket, it.key) for it in informer],
                'meaning': [(it.bucket, it.key) for it in meaning],
                }



@python_2_unicode_compatible
class StoredFile(AWSObject):
    index = models.ForeignKey(ExportIndex)
    timestamp = models.DateTimeField(auto_now=True)
    version = models.IntegerField()
    name = models.CharField(max_length=64)

    end = models.DateTimeField()

    class Meta:
        abstract = True
        unique_together = ('version', 'name', 'end',)

    def get_full_name(self):
        end = self.end.strftime('%Y-%m-%d-%H-%M-%S')
        return '{v}-{name}-to({end})'.format(v=self.version, name=self.name, end=end)

    def save(self, file, *args, **kwargs):
        if not self.key:
            self.key = self.index.key + '/' + slugify(self.get_full_name()) + '.tsv'
        self.save_from_file(filename=file)
        super(StoredFile, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class IncrementalFile(StoredFile):
    start = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('version', 'name', 'start', 'end',)

    def get_full_name(self):
        end = self.end.strftime('%Y-%m-%d-%H-%M-%S')
        start = self.start.strftime('%Y-%m-%d-%H-%M-%S') if self.start else ''
        return '{v}-{name}-to({end})-from({start})'.format(v=self.version, name=self.name, start=start, end=end)


@python_2_unicode_compatible
class OverrideFile(StoredFile):
    pass
