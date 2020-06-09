#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 23:16:47 2020

@author: chrki23
"""

import shutil


def save_image_to_file(image, dirname, suffix):
    with open('{dirname}/img_{suffix}.jpg'.format(dirname=dirname, suffix=suffix), 'wb') as out_file:
        shutil.copyfileobj(image.raw, out_file)

import requests


def download_images(prefix, dirname, links):
    length = len(links)
    for index, link in enumerate(links):
        print 'Downloading {0} of {1} images'.format(index + 1, length)
        url = prefix + link
        response = requests.get(url, stream=True)
        save_image_to_file(response, dirname, index)
        del response
 
        
 
