import copy
import csv
import pandas as pd
from datetime import datetime

# [("学生の名前", "出席 or 欠席 or 遅刻"]の形にする
member_dic = {
  "Monday": [[("ユーザ1", "出席"), ("ユーザ2", "出席"), 
                 ("ユーザ3", "出席")]
  "Tuesday": [[("ユーザ1", "出席"), ("ユーザ4", "出席"), 
                 ("ユーザ5", "出席")],
  "Wednesday": [[("ユーザ4", "出席"), ("ユーザ3", "遅刻"), 
                 ("ユーザ2", "出席")],

  "Thursday": [[("ユーザ3", "出席"), ("ユーザ1, "出席"), 
                 ("ユーザ5", "出席")]],

  "Friday": [[("ユーザ5", "欠席"), ("ユーザ4", "遅刻"), 
                 ("ユーザ2", "出席")]]]
}

#removeのMACアドレスをホスト名から探すための辞書
ip_key_dic = {}


# 割り当てられたアドレスを保持する辞書
address_dic = {
    "Tuesday": [],
    "Wednesday": [],
    "Thursday": [],
    "Friday": []
}

# 遅刻者用の割り当てられたアドレスを保持する辞書
lateness_address_dic = {
    "Tuesday": [],
    "Wednesday": [],
    "Thursday": [],
    "Friday": []
}

# identify_dicの初期化
identify_dic = {}

# 曜日の入ったリスト
days_lst = ["Tuesday", "Wednesday", "Thursday", "Friday"]

# ログデータを格納するリスト
data_lst = []

# ログデータのエクセルを読み込む関数
def csv_readr(file_path):
    # csvファイルを読み込む
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            data_lst.append(row)

# アドレス等の計算を行う関数
def cul(lst):
    # 曜日ごとのリストを初期化
    for day in days_lst:
        address_dic[day] = [[] for _ in range(len(member_dic[day]))]
        lateness_address_dic[day] = [[] for _ in range(len(member_dic[day]))]

    for data in lst:
        # 必要な情報の変数化
        print(f"data: {data}")
        if data[0] == "日付":
            print(f"data: {data[0]}")
            continue
        date_time = datetime.strptime(data[0], "%Y-%m-%dT%H:%M:%S.%f")
        log_time = date_time.strftime("%H:%M:%S")
        weekday = date_time.strftime("%A")
        dns_map = data[1]
        ip_address = data[2]
        mac_address = data[3]

        # ip_key_dicに追加
        if (dns_map == "add") and (ip_address not in ip_key_dic):
            print("aa")
            ip_key_dic[ip_address] = [mac_address]
        elif (dns_map == "add") and (ip_address in ip_key_dic):
            mac_address not in ip_key_dic[ip_address]
            ip_key_dic[ip_address].append(mac_address)

        #.strip().lower()  # MACアドレスをトリムして小文字に変換
        #print(f"mac:{mac_address}")
        #print(f"dns_map:{dns_map}")
        #print("----------")

        # 08:50以前のデータをaddress_dicの0番目のリストに追加
        if (weekday == "Saturday") or (weekday == "Sunday") or (weekday == "Monday"):
            continue

        if log_time < "08:50:00":
            if dns_map == "add":    
                address_dic[weekday][0].append(mac_address)
            elif dns_map == "remove":
                #print(date_time)
                print(f"ip_key_dicの中身: {ip_key_dic}")
                if mac_address in address_dic[weekday][0]:
                    address_dic[weekday][0].remove(mac_address)

                    try: #VMのremoveはaddの記録が残っていない為スキップ
                        del ip_key_dic[ip_address]
                    except KeyError:
                        pass
        elif log_time < "10:45:00":
        #and weekday != "Friday": #金曜日は1限のみのため
            if len(address_dic[weekday][1]) < 1:
                address_dic[weekday][1] = copy.deepcopy(address_dic[weekday][0])  
            if dns_map == "add":
                print("bb")
                address_dic[weekday][1].append(mac_address)
                if log_time < "10:30:00":
                    lateness_address_dic[weekday][0].append(mac_address) #1限の遅刻者用のアドレスリストへ追加
            elif dns_map == "remove":
                print("bc")
                #print(date_time)
                #print(f"ip_key_dicの中身: {ip_key_dic}")
                if mac_address in address_dic[weekday][1]:
                    address_dic[weekday][1].remove(mac_address)
                    try:
                        del ip_key_dic[ip_address]
                    except KeyError:
                        pass
        elif log_time < "13:15:00": #火曜日のみ3限があるため
            print("c")  
            if dns_map == "add" and weekday == "Tuesday":
                if len(address_dic[weekday][1]) < 1:
                    address_dic[weekday][2] = copy.deepcopy(address_dic[weekday][1])
                address_dic[weekday][2].append(mac_address)
            elif dns_map == "add" and weekday != "Tuesday": 
                if log_time < "12:25:00":
                    lateness_address_dic[weekday][1].append(mac_address) #1限の遅刻者用のアドレスリストへ追加
            elif dns_map == "remove" and weekday == "Tuesday":
                #print(date_time)
                #print(f"ip_key_dicの中身: {ip_key_dic}")
                print("333")
                mac_address = ip_key_dic[ip_address]
                print(f"weekday: {weekday}")
                if mac_address in address_dic[weekday][2]:
                    address_dic[weekday][2].remove(mac_address)
                    try:
                        del ip_key_dic[ip_address]
                    except KeyError:
                        pass

# 曜日の入ったリスト
days_lst = ["Tuesday", "Wednesday", "Thursday", "Friday"]

# identify_dicの初期化
identify_dic = {}

#学生の名前をidentify_dicへ追加
def compare_all_members():
    for day in days_lst:
        for member_list in member_dic[day]:
            for member_info in member_list:
                name = member_info[0]
                sit_attend = member_info[1]
                if sit_attend == "欠席":
                    continue
                print(f"day:{day}, name:{name}, sit_attend:{sit_attend}")
                if name not in identify_dic:
                    identify_dic[name] = set()
                compare_name(name)

# 指定された名前が含まれるリストを比較する関数
def compare_name(name):
    comparison_targets = []
    common_addresses = set()

    # 引数nameが受講している授業の曜日と時限をcomparison_targetsに格納する
    for day in days_lst:
        for i, member_list in enumerate(member_dic[day]):
            print(f"member_list: {member_list}, i: {i}, name: {name}, type: {type(name)}")
            for member in member_list:
                if name in member:
                    print(f"member: {member}")
                    gakusei, sit_attend = member
                    if sit_attend == "遅刻":
                        lst_name = "lateness_address_dic"
                        comparison_targets.append((day, i, lst_name))
                    elif sit_attend == "出席":
                        lst_name = "address_dic"
                        comparison_targets.append((day, i, lst_name))
                else:
                    pass
                    #print(f"name:{name}, member_lst;{member_list}")

    # 指定された名前が含まれるリスト間での比較
    for base_day, base_index, base_lst_name in comparison_targets:
        print(f"base_lst_name: {base_lst_name}")
        base_lst_name = globals()[base_lst_name]
        base_address_list = set(base_lst_name[base_day][base_index])  # セットに変換して重複を削除
        #print(f"base_address_list: {base_address_list}")

        if len(comparison_targets) < 2:
            identify_dic[name].update(base_address_list)
        
        for compare_day, compare_index, compare_lst_name in comparison_targets:
            print(f"compare_lst_name: {compare_lst_name}")
            compare_lst_name = globals()[compare_lst_name]
            compare_address_list = set(compare_lst_name[compare_day][compare_index])
            if base_day == compare_day and base_index == compare_index:
                continue  # 同じリストの場合はスキップ
            print("---------------")
            print(f"base_day: {base_day}, base_index: {base_index}, name: {name}")
            print(f"compare_day: {compare_day}, compare_index: {compare_index}")
            print(f"base_address_list: {base_address_list}")
            print(f"compare_address_list: {compare_address_list}")
            common_elements = base_address_list.intersection(compare_address_list)
            print(f"common_ele:{common_elements}")
            if common_addresses:
                common_addresses = common_addresses.intersection(common_elements)
            else:
                common_addresses.update(common_elements)
    identify_dic[name].update(common_addresses)

if __name__ == "__main__":
    # DDNS-DHCPログのCSVファイルのパス
    csv_path = "./ddns-dhcp-log.csv"

    # 保存するtxtファイルのパス
    write_file = "./test.txt"

    # エクセルファイルを読み込む
    csv_readr(csv_path)

    #print(f"data_lst:{data_lst}")
    #print("---------")
    #print(data_lst[0][3])

    # アドレス等の計算を行う
    cul(data_lst)

    # すべてのメンバーのリストを比較する
    compare_all_members()

    # identify_dicの結果を表示
    print("----------")
    with open(write_file, mode='w') as write_file:
        for name, addresses in identify_dic.items():
            print(f"{name}: {addresses}", file=write_file)  # file引数を使用
