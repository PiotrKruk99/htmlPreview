#!/usr/bin/env python3

from os.path import isfile, abspath, getmtime
from argparse import ArgumentParser, ArgumentTypeError
from selenium.webdriver import Firefox
from time import sleep


def toFloat(value):
    value = value.replace(',', '.')

    try:
        value = float(value)
    except ValueError:
        raise ArgumentTypeError('argument is not a number')

    if value < 0:
        raise ArgumentTypeError('argument must be not negative number')
    return value


parser = ArgumentParser()
parser.description = 'Script for opening in browser and autorefreshing html file on change.'
parser.add_argument('name', help='html file to be open')
#parser.add_argument('-r', '--rate', type=float, default=2.0, help='time between file state check in seconds')
parser.add_argument('-r', '--rate', type=toFloat, default=2.0,
                    help='time between file state checks in seconds, only float non negative numbers acceptable')

args = parser.parse_args()

if not isfile(args.name):
    print('script argument is not an existing file path')
    quit()

path = abspath(args.name)

driver = Firefox(executable_path='./geckodriver')
driver.get('file://' + path)

lastModified = getmtime(args.name)

while True:
    sleep(args.rate)

    try:
        # throw exception when browser page is closed and quit script
        test = driver.window_handles
    except BaseException as e:
        quit()

    modTime = getmtime(args.name)
    if modTime > lastModified:
        driver.refresh()
        lastModified = modTime
