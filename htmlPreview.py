#!/usr/bin/env python3

from os import path
from os.path import isfile
from os.path import abspath
from os.path import getmtime
from argparse import ArgumentParser
from selenium.webdriver import Firefox
from time import sleep

parser = ArgumentParser()
parser.description = 'Script for opening in browser and autorefreshing html file on change.'
parser.add_argument('name', help='html file to be open')

args = parser.parse_args()

if not isfile(args.name):
    print('script argument is not an existing file path')
    quit()

path = abspath(args.name)

driver = Firefox(executable_path='./geckodriver')
driver.get('file://' + path)

lastModified = getmtime(args.name)

while True:
    sleep(2)

    try:
        test = driver.window_handles # throw exception when browser page is closed and quit script
    except BaseException as e:
        quit()

    modTime = getmtime(args.name)
    if modTime > lastModified:
        driver.refresh()
        lastModified = modTime