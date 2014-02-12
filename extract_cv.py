#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2014 Stefano Costa <steko@iosa.it>
# 
# To the extent possible under law, Stefano Costa has waived all
# copyright and related or neighboring rights to this work. This work
# is published from: Italia.

import csv

import lxml
import grequests
import scraperwiki



def extract_birth(cvfile):
    '''Extract birth year from PDF file with CV.'''

    pdf = open(CVFILE, 'rb')
    xml = scraperwiki.pdftoxml(pdf.read())

    root = lxml.etree.fromstring(xml)
    birthstr = root.xpath('//text[@top="320"]')[0].text
    
    mf = 'M' if birthstr[3] == 'o' else 'F'
    birthyear = birthstr[-4:]
    
    print(mf, birthyear)


def save_cv(response, **kwargs):
    '''Download a CV and save it to disk.'''

    filename = response.headers['content-disposition'].split('=')[-1].strip('"')

    with open(filename, 'wb') as f:
        f.write(response.content)
        print(filename)


def list_ids(csvfile):
    with open(csvfile, 'rb') as f:
        reader = csv.DictReader(f)
        CVURL = 'https://abilitazione.cineca.it/ministero.php/public/getfile/domanda/%d/tipo/1'
        for row in reader:
            yield CVURL % int(row['id'])


def main():
    urls = list_ids('candidates.csv')
    rs = (grequests.get(u, hooks=dict(response=save_cv)) for u in urls)
    grequests.map(rs)

main()
