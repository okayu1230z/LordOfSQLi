# orc

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
https://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw=aa
```

とすると

```
query : select id from prob_orc where id='admin' and pw='aa'
```

となった。
コードを読んでいく。

```
if(preg_match('/ /i', $_GET[pw])) exit("No whitespace ~_~");
```

待ってました！whitespaceフィルター！

```

```

今回はたまたま瞬殺でした。


## supplementary

いろんな文字がフィルターされたときの代替文字（CTF界伝説のサイト、[こちら](https://graneed.hatenablog.com/entry/2018/10/26/232304)を参照）

- ' : "
- 半角スペース : タブ文字
- = : STRCMPとis not TRUE
- or : ||
- admin : "admi" "n" を文字列結合

## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [BSides Delhi CTF 2018 Write up | こんとろーるしーこんとろーるぶい](https://graneed.hatenablog.com/entry/2018/10/26/232304)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)