#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PIL.ExifTags
import PIL.Image

import fnmatch
import os
import os.path
import re
import shutil
import distutils
from distutils import dir_util


def move_if(fname, match_dir, not_match_dir):
    patterns = ['whatsup', 'WhatsApp']
    whatsup = False
    for p in patterns:
        if p in fname:
            whatsup = True
            break
    shutil.copy2(fname, match_dir if whatsup else not_match_dir)



includes = [
    '*.jpg',
    '*.JPG',
    '*.jpeg',
    '*.png',
    '*.mp4',
    '*.MTS'
] # for files only
excludes = [
    '/home/user/data/data/Pictures/walls',
    '/home/user/data/data/Pictures/Я (для резюме)'
    ] # for dirs and files

targets = {
    '0_sorted_dir' : '/home/user/data/data/Pictures/0_sorted',
    '0_unsorted_dir' : '/home/user/data/data/Pictures/0_unsorted',
    '0_whatsup_dir' : '/home/user/data/data/Pictures/0_whatsup',
    '0_videos' : '/home/user/data/data/Pictures/0_videos',
    '0_other' : '/home/user/data/data/Pictures/0_other',
}
for k,v in targets.iteritems():
    if (os.path.isdir(v)):
        shutil.rmtree(v)
    distutils.dir_util.mkpath(v)
    excludes.append(v)

    # transform glob patterns to regular expressions
includes = r'|'.join([fnmatch.translate(x) for x in includes])
excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'


for root, dirs, files in os.walk('/home/user/data/data/Pictures'):
    # exclude dirs
    dirs[:] = [os.path.join(root, d) for d in dirs]
    dirs[:] = [d for d in dirs if not re.match(excludes, d)]

    # exclude/include files
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if not re.match(excludes, f)]
    files = [f for f in files if re.match(includes, f)]

    for fname in files:

        fpath, fext = os.path.splitext(fname)
        if fext in ['.png']:
            shutil.copy2(fname, targets['0_other'])
            continue
        elif fext in ['.mp4', '.MTS']:
            shutil.copy2(fname, targets['0_videos'])
            continue

        try:
            img = PIL.Image.open(fname)
            if img._getexif():
                exif = {
                    PIL.ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS
                }
                try:
                    datetime = exif['DateTime']
                    date, time = datetime.split(' ')
                    year, month, day = date.split(':')
                    print '{0}: {1}/{2}/{3}'.format(fname, year, month, day)
                    fname_target_dir = '/'.join([targets['0_sorted_dir'], year, month, day])
                    distutils.dir_util.mkpath(fname_target_dir)
                    # shutil.copy2(fname, '/'.join([fname_target_dir, os.path.basename(fname)]))
                    shutil.copy2(fname, fname_target_dir)
                except KeyError as e:
                    print 'No DateTime key in exif for {0}'.format(fname)
                    move_if(fname, targets['0_whatsup_dir'], targets['0_unsorted_dir'])
            else:
                print 'No _getexif for {0}'.format(fname)
                move_if(fname, targets['0_whatsup_dir'], targets['0_unsorted_dir'])
        except IOError as e:
            print 'Cannot work with {0} ({1})'.format(fname, e)
            move_if(fname, targets['0_whatsup_dir'], targets['0_unsorted_dir'])



        # GPS coord info (for future, append place description inplace with day number)
        # gpsinfo = {}
        # for key in exif['GPSInfo'].keys():
        #     decode = PIL.ExifTags.GPSTAGS.get(key,key)
        #     gpsinfo[decode] = exif['GPSInfo'][key]
        # print gpsinfo
