import asyncio  # 异步IO
import math
from datetime import datetime, time, timedelta, timezone

import pyautogui  # 操控鼠标键盘
import pyperclip  # 复制到剪贴板（因为pyautogui不支持输入中文，所以用pyperclip先把中文复制到剪贴板，再使用pyautogui按ctrl+v粘贴）
from aiohttp import ClientSession, ClientTimeout  # 异步HTTP
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # 异步定时任务
from apscheduler.triggers.cron import CronTrigger

room_id_list = [
    # -------------------------------------------------- =LOVE -------------------------------------------------- #
    "107419",  # 大谷 映美里（=LOVE）
    "107470",  # 大場 花菜（=LOVE）
    "106820",  # 音嶋 莉沙（=LOVE）
    "106267",  # 齋藤 樹愛羅（=LOVE）
    "106268",  # 佐々木 舞香（=LOVE）
    "106270",  # 髙松 瞳（=LOVE）
    "107457",  # 瀧脇 笙古（=LOVE）
    "106016",  # 野口 衣織（=LOVE）
    "106264",  # 諸橋 沙夏（=LOVE）
    "105923",  # 山本 杏奈（=LOVE）
    # -------------------------------------------------- ≠ME -------------------------------------------------- #
    "230189",  # 尾木 波菜（≠ME）
    "230161",  # 落合 希来里（≠ME）
    "230160",  # 蟹沢 萌子（≠ME）
    "228540",  # 河口 夏音（≠ME）
    "230185",  # 川中子 奈月心（≠ME）
    "230164",  # 櫻井 もも（≠ME）
    "230175",  # 菅波 美玲（≠ME）
    "230181",  # 鈴木 瞳美（≠ME）
    "230174",  # 谷崎 早耶（≠ME）
    "230219",  # 冨田 菜々風（≠ME）
    "230208",  # 永田 詩央里（≠ME）
    "230171",  # 本田 珠由記（≠ME）
    # -------------------------------------------------- ≒JOY -------------------------------------------------- #
    "387113",  # 逢田 珠里依（≒JOY）
    "387127",  # 天野 香乃愛（≒JOY）
    "387845",  # 市原 愛弓（≒JOY）
    "387812",  # 江角 怜音（≒JOY）
    "387179",  # 大信田 美月（≒JOY）
    "387187",  # 大西 葵（≒JOY）
    "150710",  # 小澤 愛実（≒JOY）
    "387836",  # 髙橋 舞（≒JOY）
    "387164",  # 藤沢 莉子（≒JOY）
    "387863",  # 村山 結香（≒JOY）
    "387209",  # 山田 杏佳（≒JOY）
    "387814",  # 山野 愛月（≒JOY）
    # -------------------------------------------------- 官方直播间 -------------------------------------------------- #
    "139470",  # =LOVE 官方直播间
    "272301",  # ≠ME 官方直播间
    "402345",  # ≒JOY 官方直播间
]

room_status_list = [1] * len(room_id_list)  # 1：未开播，2：已开播，3：已开启投票直播

room_end_time_list = [0] * len(room_id_list)

birthday_list = [
    # -------------------------------------------------- =LOVE -------------------------------------------------- #
    {"name": "大谷 映美里（=LOVE）", "birthday": "03.15"},
    {"name": "大場 花菜（=LOVE）", "birthday": "02.04"},
    {"name": "音嶋 莉沙（=LOVE）", "birthday": "08.11"},
    {"name": "齋藤 樹愛羅（=LOVE）", "birthday": "11.26"},
    {"name": "佐々木 舞香（=LOVE）", "birthday": "01.21"},
    {"name": "髙松 瞳（=LOVE）", "birthday": "01.19"},
    {"name": "瀧脇 笙古（=LOVE）", "birthday": "07.09"},
    {"name": "野口 衣織（=LOVE）", "birthday": "04.26"},
    {"name": "諸橋 沙夏（=LOVE）", "birthday": "08.03"},
    {"name": "山本 杏奈（=LOVE）", "birthday": "11.30"},
    # -------------------------------------------------- ≠ME -------------------------------------------------- #
    {"name": "尾木 波菜（≠ME）", "birthday": "05.08"},
    {"name": "落合 希来里（≠ME）", "birthday": "05.22"},
    {"name": "蟹沢 萌子（≠ME）", "birthday": "10.25"},
    {"name": "河口 夏音（≠ME）", "birthday": "07.29"},
    {"name": "川中子 奈月心（≠ME）", "birthday": "09.26"},
    {"name": "櫻井 もも（≠ME）", "birthday": "04.13"},
    {"name": "菅波 美玲（≠ME）", "birthday": "02.05"},
    {"name": "鈴木 瞳美（≠ME）", "birthday": "04.13"},
    {"name": "谷崎 早耶（≠ME）", "birthday": "10.07"},
    {"name": "冨田 菜々風（≠ME）", "birthday": "07.17"},
    {"name": "永田 詩央里（≠ME）", "birthday": "04.02"},
    {"name": "本田 珠由記（≠ME）", "birthday": "02.27"},
    # -------------------------------------------------- ≒JOY -------------------------------------------------- #
    {"name": "逢田 珠里依（≒JOY）", "birthday": "09.13"},
    {"name": "天野 香乃愛（≒JOY）", "birthday": "01.21"},
    {"name": "市原 愛弓（≒JOY）", "birthday": "08.21"},
    {"name": "江角 怜音（≒JOY）", "birthday": "04.26"},
    {"name": "大信田 美月（≒JOY）", "birthday": "09.27"},
    {"name": "大西 葵（≒JOY）", "birthday": "08.06"},
    {"name": "小澤 愛実（≒JOY）", "birthday": "04.09"},
    {"name": "髙橋 舞（≒JOY）", "birthday": "02.22"},
    {"name": "藤沢 莉子（≒JOY）", "birthday": "01.16"},
    {"name": "村山 結香（≒JOY）", "birthday": "02.15"},
    {"name": "山田 杏佳（≒JOY）", "birthday": "02.02"},
    {"name": "山野 愛月（≒JOY）", "birthday": "10.21"},
    # -------------------------------------------------- 指P -------------------------------------------------- #
    {"name": "指原 莉乃", "birthday": "11.21"}
]

message_queue = asyncio.Queue()  # 异步消息队列

semaphore = asyncio.Semaphore(10)  # 限制并发数

default_timeout = ClientTimeout(total=3)

JST = timezone(timedelta(hours=9))  # 日本时区


# -------------------------------------------------- 爬虫1：检查直播状态 -------------------------------------------------- #
async def get_room_info(room_id, session):
    # api文档：https://qiita.com/takeru7584/items/f4ba4c31551204279ed2
    room_url = f"https://www.showroom-live.com/api/live/live_info?room_id={room_id}"
    try:
        async with session.get(room_url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"爬取 showroom {room_id} 失败：status {response.status}")
                return None
    except Exception as e:
        print(f"爬取 showroom {room_id} 出错：{str(e)}")
        return None


async def limited_get_room_info(room_id, session):
    async with semaphore:
        return await get_room_info(room_id, session)


async def run_spider_1():
    # 当前时间转为日本时间，如果是在凌晨0点到5点之间，那么就不用运行，因为这是睡觉时间不可能开播
    current_time = datetime.now(JST).time()
    if time(0, 3) < current_time < time(4, 55):
        return

    async with ClientSession(timeout=default_timeout) as session:
        tasks = [limited_get_room_info(room_id, session) for room_id in room_id_list]
        response_list = await asyncio.gather(*tasks)

        message = ""

        for i, response in enumerate(response_list):
            if response is None:
                continue

            if room_status_list[i] == 1 and response["live_status"] == 2:  # 原来没开播，现在开播了
                if math.floor(datetime.now().timestamp()) - room_end_time_list[i] > 5 * 60:
                    message += f"{response["room_name"]}\n▶️ 直播中！\n\n"
                    room_status_list[i] = response["live_status"]
                    print(f"{response["room_name"]} 已开播")
                else:
                    room_status_list[i] = response["live_status"]
                    print(f"{response["room_name"]} 断线重连")
            elif room_status_list[i] == 2 and response["live_status"] == 1:  # 原来已开播，现在下播了
                room_status_list[i] = response["live_status"]
                room_end_time_list[i] = math.ceil(datetime.now().timestamp())
                print(f"{response["room_name"]} 已下播")
            elif room_status_list[i] == 2 and response["live_status"] == 2:  # 原来已开播，现在直播中
                pass
            elif room_status_list[i] == 1 and response["live_status"] == 1:  # 原来没开播，现在也没开播
                pass
            elif room_status_list[i] == 1 and response["live_status"] == 3:  # 原来没开播，现在开启投票直播
                if math.floor(datetime.now().timestamp()) - room_end_time_list[i] > 5 * 60:
                    message += f"{response["room_name"]}\n▶️ 直播中！（投票直播）\n\n"
                    room_status_list[i] = response["live_status"]
                    print(f"{response["room_name"]} 已开启投票直播")
                else:
                    room_status_list[i] = response["live_status"]
                    print(f"{response["room_name"]} 断线重连")
            elif room_status_list[i] == 3 and response["live_status"] == 1:  # 原来在投票直播，现在下播了
                room_status_list[i] = response["live_status"]
                room_end_time_list[i] = math.ceil(datetime.now().timestamp())
                print(f"{response["room_name"]} 已下播")
            elif room_status_list[i] == 2 and response["live_status"] == 3:  # 原来已开播，现在开启投票
                room_status_list[i] = response["live_status"]
                print(f"{response["room_name"]} 已开启投票")
            elif room_status_list[i] == 3 and response["live_status"] == 2:  # 原来在投票直播，现在结束投票但仍在直播中
                room_status_list[i] = response["live_status"]
                print(f"{response["room_name"]} 已结束投票但仍在直播中")
            elif room_status_list[i] == 3 and response["live_status"] == 3:  # 原来在投票直播，现在也在投票直播
                pass
            else:
                print(f"警告：未知直播状态！{response["live_status"]}")

        if message:
            await message_queue.put(message)

        print("showroom 最后检查时间：" + datetime.now().strftime("%Y.%m.%d %H:%M:%S"))


# -------------------------------------------------- 爬虫2：检查生日 -------------------------------------------------- #
async def run_spider_2():
    message = ""

    # 转为日本时间：UTC+9
    today = datetime.now(JST).strftime("%m.%d")

    for person in birthday_list:
        if person["birthday"] == today:
            message += f"{person["name"]}\n🎂 生日快乐！\n\n"
            print(f"{person["name"]} 今天生日")

    if message:
        message += f"{today}\n\n"
        await message_queue.put(message)


# -------------------------------------------------- 消息发送 -------------------------------------------------- #
async def send_message():
    while True:
        # 阻塞式消费，避免轮询
        message = await message_queue.get()
        message += datetime.now().strftime("%H:%M:%S")
        pyperclip.copy(message)

        # 点击置顶的第一个群聊，防止QQ重启后焦点不在该群聊窗口
        try:
            pyautogui.click(x=2300, y=280)
        except Exception as e:
            print(f"点击失败：{str(e)}")
            continue
        await asyncio.sleep(1)  # 给切换窗口预留时间

        # 发送消息
        try:
            pyautogui.click(x=2666, y=1777)
        except Exception as e:
            print(f"点击失败：{str(e)}")
            continue
        await asyncio.sleep(0.5)  # 给一点反应时间
        pyautogui.hotkey("ctrl", "v")
        await asyncio.sleep(0.5)  # 给一点反应时间
        pyautogui.hotkey("enter")

        print("消息已发送，当前时间：" + datetime.now().strftime("%H:%M:%S"))
        await asyncio.sleep(1)  # 防止QQ发送消息过快


# -------------------------------------------------- 主程序 -------------------------------------------------- #
async def main():
    # 启动调度器（生产者）
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_spider_1, trigger=CronTrigger(second=0))  # 每分钟执行一次
    scheduler.add_job(run_spider_2, trigger=CronTrigger(hour=23))  # 每天晚上11点执行一次
    scheduler.start()
    print("定时任务已启动")

    # 启动消息发送（消费者）
    await asyncio.gather(send_message(), return_exceptions=True)  # 设置为True，防止单个协程崩溃影响整体


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序已终止")
