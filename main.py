import time
from datetime import datetime

import pyautogui
import pyperclip
import requests


def print_hello_world():
    print("Hello World")

    # 房间ID列表
    room_id_list = [
        "107419", "107470", "106820", "106267", "106268",
        "106270", "107457", "106016", "106264", "105923",
        "230189", "230161", "230160", "228540", "230185", "230164",
        "230175", "230181", "230174", "230219", "230208", "230171",
        "387113", "387127", "387845", "387812", "387179", "387187",
        "150710", "387836", "387164", "387863", "387209", "387814",
        "139470", "272301", "402345",
        "61774"
    ]

    # 初始化直播状态列表和结束时间列表
    live_status_list = [1] * len(room_id_list)
    live_end_time_list = [0] * len(room_id_list)

    # 生日信息
    birthday_month_list = [
        3, 2, 8, 11, 1,
        1, 7, 4, 8, 11,
        5, 5, 10, 7, 9, 4,
        2, 4, 10, 7, 4, 2,
        9, 1, 8, 4, 9, 8, 4,
        2, 1, 2, 2, 10, 11
    ]
    birthday_day_list = [
        15, 4, 11, 26, 21,
        19, 9, 26, 3, 30,
        8, 22, 25, 29, 26, 13,
        5, 13, 7, 17, 2, 27,
        13, 21, 21, 26, 27, 6,
        9, 22, 16, 15, 2, 21, 21
    ]

    birthday_status_list = [2023] * len(birthday_month_list)

    # 成员列表
    member_list = [
        "大谷 映美里（=LOVE）", "大場 花菜（=LOVE）", "音嶋 莉沙（=LOVE）", "齋藤 樹愛羅（=LOVE）", "佐々木 舞香（=LOVE）",
        "髙松 瞳（=LOVE）", "瀧脇 笙古（=LOVE）", "野口 衣織（=LOVE）", "諸橋 沙夏（=LOVE）", "山本 杏奈（=LOVE）",
        "尾木 波菜（≠ME）", "落合 希来里（≠ME）", "蟹沢 萌子（≠ME）", "河口 夏音（≠ME）", "川中子 奈月心（≠ME）",
        "櫻井 もも（≠ME）",
        "菅波 美玲（≠ME）", "鈴木 瞳美（≠ME）", "谷崎 早耶（≠ME）", "冨田 菜々風（≠ME）", "永田 詩央里（≠ME）", "本田 珠由記（≠ME）",
        "逢田 珠里依（≒JOY）", "天野 香乃愛（≒JOY）", "市原 愛弓（≒JOY）", "江角 怜音（≒JOY）", "大信田 美月（≒JOY）",
        "大西 葵（≒JOY）",
        "小澤 愛実（≒JOY）", "髙橋 舞（≒JOY）", "藤沢 莉子（≒JOY）", "村山 結香（≒JOY）", "山田 杏佳（≒JOY）", "山野 愛月（≒JOY）",
        "指原 莉乃"
    ]

    while True:
        send = ""

        for i in range(len(room_id_list)):
            try:
                respond = requests.get(f"https://www.showroom-live.com/api/live/live_info?room_id={room_id_list[i]}")
            except Exception as e:
                print(e)
                time.sleep(30)
                continue

            if respond.status_code != 200:
                print(respond.status_code)
                time.sleep(30)
                continue

            try:
                json = respond.json()
            except Exception as e:
                print(e)
                time.sleep(30)
                continue

            if live_status_list[i] == 1 and json['live_status'] == 2:
                if time.time() - live_end_time_list[i] > 5 * 60:
                    send += f"{json['room_name']}\n▶️ 直播中！\n\n"
                    live_status_list[i] = json['live_status']
                    print(f"{json['room_name']} 已开播")
                else:
                    live_status_list[i] = json['live_status']
                    print(f"{json['room_name']} 疑似断线重连")
            elif live_status_list[i] == 2 and json['live_status'] == 1:
                live_status_list[i] = json['live_status']
                live_end_time_list[i] = time.time()
                print(f"{json['room_name']} 已下播")
            elif live_status_list[i] == 2 and json['live_status'] == 2:
                print(f"{json['room_name']} ✓")
            elif live_status_list[i] == 1 and json['live_status'] == 1:
                print(json['room_name'])

            if i == len(room_id_list) - 1:
                date = datetime.now()
                year = date.year

                for j in range(len(birthday_month_list)):
                    if year > birthday_status_list[j]:
                        birthday_date = datetime(year, birthday_month_list[j], birthday_day_list[j])
                        offset = time.time() - (birthday_date.timestamp() - 1 * 60 * 60)

                        if 0 <= offset < 24 * 60 * 60:
                            send += f"{member_list[j]}\n🎂 生日快乐！\n{year}.{birthday_date.month}.{birthday_date.day}\n\n"
                            birthday_status_list[j] = year
                            print(f"{member_list[j]} 生日快乐！")

            time.sleep(0.1)  # 象征性休眠一会儿

        if send == "":
            pyautogui.click(x=715, y=1775)  # 如果待发送内容为空，点击屏幕，防止手机熄屏
        else:
            date = datetime.now()
            send += date.strftime("%H:%M:%S")
            pyperclip.copy(send)
            pyautogui.click(x=715, y=1775)
            time.sleep(0.1)
            pyautogui.hotkey('Ctrl', 'V')
            time.sleep(0.1)
            pyautogui.hotkey('enter')

        date = datetime.now()
        print(date.strftime("%H:%M:%S"))

        time.sleep(30)


if __name__ == "__main__":
    print_hello_world()
