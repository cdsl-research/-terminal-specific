# -terminal-specific
- DHCPサーバを用いてユーザの所有する端末を特定するソフトウェアです．

- identify.pyの"member_dic"の中身に，各学生の一週間の授業の出席状況と学生名を記述する．
- また，main関数のcsv_pathにはDDNS・DHCPログのファイルパスを記述する．
- その後，identify.pyを実行すると各学生の名前とその学生が所有するMACアドレスがtxtファイルに記述される（ない場合は生成される）
```identify.pyを実行
sora@c0a21021-ex:~/late_period$ python3 identify.py
```

```出力先ファイルのtxtファイル
ユーザ1: {'22:e7:ec:a3:24:dd'}
ユーザ4: set('3a:f1:07:9d:47:c1')
ユーザ5: {'26:5c:3f:ce:45:a5'}
ユーザ3: set('f2:ba:d9:ef:c7:ee')
ユーザ2: {'22:e8:21:dd:6b:42'}
```
