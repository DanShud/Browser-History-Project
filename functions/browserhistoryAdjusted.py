"""This is a file taken
https://github.com/kcp18/browserhistory 
I made a few adjustments to add typed count to db

we couldn't get this file to work properly as it assumes everyone has a defualt user but this is not always the case/
"""


import csv
import os
import sqlite3
import sys
from datetime import datetime
from typing import Counter


# platform_table maps the name of user's OS to a platform code
platform_table = {
        'linux': 0,
        'linux2': 0,
        'darwin': 1,
        'cygwin': 2,
        'win32': 2,
        }

# it supports Linux, MacOS, and Windows platforms.
try:
    user_platformcode = platform_table[sys.platform]
except KeyError:
    class NotAvailableOS(Exception):
        pass
    raise NotAvailableOS("It does not support your OS.")


def get_username() -> str:
    """
    Get username based on their local computers
    """
    platform_code = user_platformcode
    cwd_path = os.getcwd()
    cwd_path_list = []
    # if it is a macOS
    if platform_code == 1:
        cwd_path_list = cwd_path.split('/')
    # if it is a windows
    elif platform_code == 2:
        cwd_path_list = cwd_path.split('\\')
    # if it is a linux
    else:
        cwd_path_list = cwd_path.split('/')
    return cwd_path_list[2]


def get_database_paths() -> dict:
    """
    Get paths to the database of browsers and store them in a dictionary.
    It returns a dictionary: its key is the name of browser in str and its value is the path to database in str.
    """
    platform_code = user_platformcode
    browser_path_dict = dict()
    # if it is a macOS
    if platform_code == 1:
        cwd_path = os.getcwd()
        cwd_path_list = cwd_path.split('/')
        # it creates string paths to broswer databases
        abs_safari_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2], 'Library', 'Safari', 'History.db')
        abs_chrome_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2], 'Library', 'Application Support', 'Google/Chrome/Default', 'History')
        abs_firefox_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2], 'Library', 'Application Support', 'Firefox/Profiles')
        # check whether the databases exist
        if os.path.exists(abs_safari_path):
            browser_path_dict['safari'] = abs_safari_path
        if os.path.exists(abs_chrome_path):
            browser_path_dict['chrome'] = abs_chrome_path
        if os.path.exists(abs_firefox_path):
            firefox_dir_list = os.listdir(abs_firefox_path)
            # it looks for a directory that ends '.default'
            for f in firefox_dir_list:
                if f.find('.default') > 0:
                    abs_firefox_path = os.path.join(abs_firefox_path, f, 'places.sqlite')
            # check whether the firefox database exists
            if os.path.exists(abs_firefox_path):
                browser_path_dict['firefox'] = abs_firefox_path
    # if it is a windows
    if platform_code == 2:
        homepath = os.path.expanduser("~")
        abs_chrome_path = os.path.join(homepath, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History')
        abs_firefox_path = os.path.join(homepath, 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles')
        # it creates string paths to broswer databases
        if os.path.exists(abs_chrome_path):
            browser_path_dict['chrome'] = abs_chrome_path
        if os.path.exists(abs_firefox_path):
            firefox_dir_list = os.listdir(abs_firefox_path)
            for f in firefox_dir_list:
                if f.find('.default') > 0:
                    abs_firefox_path = os.path.join(abs_firefox_path, f, 'places.sqlite')
            if os.path.exists(abs_firefox_path):
                browser_path_dict['firefox'] = abs_firefox_path
    # if it is a linux and it has only a firefox
    if platform_code == 0:
        cwd_path = os.getcwd()
        cwd_path_list = cwd_path.split('/')
        # it creates string paths to broswer databases
        abs_firefox_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2], '.mozilla', 'firefox')
        # check whether the path exists
        if os.path.exists(abs_firefox_path):
            firefox_dir_list = os.listdir(abs_firefox_path)
            # it looks for a directory that ends '.default'
            for f in firefox_dir_list:
                if f.find('.default') > 0:
                    abs_firefox_path = os.path.join(abs_firefox_path, f, 'places.sqlite')
            # check whether the firefox database exists
            if os.path.exists(abs_firefox_path):
                browser_path_dict['firefox'] = abs_firefox_path

    return browser_path_dict


def get_browserhistory(limit=None, historyPath=None) -> dict:
    """Get the user's browsers history by using sqlite3 module to connect to the dabases.
       It returns a dictionary: its key is a name of browser in str and its value is a list of
       tuples, each tuple contains four elements, including url, title, and visited_time. 

       Example
       -------
       >>> import browserhistory as bh
       >>> dict_obj = bh.get_browserhistory()
       >>> dict_obj.keys()
       >>> dict_keys(['safari', 'chrome', 'firefox'])
       >>> dict_obj['safari'][0]
       >>> ('https://mail.google.com', 'Mail', '2018-08-14 08:27:26')
    """
    # browserhistory is a dictionary that stores the query results based on the name of browsers.
    browserhistory = {}

    # call get_database_paths() to get database paths.
    paths2databases = {'chrome':  historyPath}
    print(paths2databases)
    counter= 0 
    for browser, path in paths2databases.items():
        try:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            _SQL = ''
            # SQL command for browsers' database table
            if browser == 'chrome':
                _SQL = f"""SELECT url, title, visit_count, typed_count, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') 
                                    AS last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT {limit}"""
            # query_result will store the result of query
            query_result = []
            try:
                cursor.execute(_SQL)
                query_result = cursor.fetchall()
            except sqlite3.OperationalError:
                print('* Notification * ')
                print('Please Completely Close ' + browser.upper() + ' Window')
            except Exception as err:
                print(err)
            # close cursor and connector
            cursor.close()
            conn.close()
            # put the query result based on the name of browsers.
            browserhistory[browser] = query_result
        except sqlite3.OperationalError:
            print('* ' + browser.upper() + ' Database Permission Denied.')
    return browserhistory


def write_browserhistory_csv(limit=None) -> None:
    """It writes csv files that contain the browser history in
    the current working directory. It will writes csv files base on
    the name of browsers the program detects."""
    browserhistory = get_browserhistory(limit)
    counter = 0
    for browser, history in browserhistory.items():
        with open(browser + '_history.csv', mode='w', encoding='utf-8', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',',
                            quoting=csv.QUOTE_ALL)
            for data in history:
                csv_writer.writerow(data)
            print(counter)
            counter+=1 
            if limit != None or counter >= limit:
                pass

       
def write_browserhistory_toArray(limit=None) -> None:
    """writes to SQL db"""
    browserhistory = get_browserhistory(limit)
    counter = 0
    
    for browser, history in browserhistory.items():
        with open(browser + '_history.csv', mode='w', encoding='utf-8', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',',
                            quoting=csv.QUOTE_ALL)
            for data in history:
                csv_writer.writerow(data)
            print(counter)
            counter+=1 
            if limit != None and counter >= limit:
                pass
    return browserhistory