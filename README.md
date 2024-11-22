# -terminal-specific
- DHCPサーバを用いてユーザの所有する端末を特定するソフトウェアです．

- identify.pyの"member_dic"の中身に，各学生の一週間の授業の出席状況と学生名を記述する．
- また，main関数のcsv_pathにはDDNS・DHCPログのファイルパスを記述する．
- その後，identify.pyを実行すると各学生の名前とその学生が所有するMACアドレスがtxtファイルに記述される（ない場合は生成される）
```identify.pyを実行
sora@c0a21021-ex:~/late_period$ python3 identify.py
```

```出力先ファイルのtxtファイル
ユーザ1: {'スマホのMACアドレス','PCのMACアドレス'}
ユーザ2: {'スマホのMACアドレス','PCのMACアドレス'}
ユーザ3: {'スマホのMACアドレス','PCのMACアドレス'}
ユーザ4:{'スマホのMACアドレス','PCのMACアドレス'}
ユーザ5:{'スマホのMACアドレス','PCのMACアドレス'}
```
