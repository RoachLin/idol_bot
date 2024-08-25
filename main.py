import asyncio  # 异步
import math
from datetime import datetime, timezone, timedelta, time

import aiohttp  # 异步HTTP
import pyautogui  # 操控鼠标键盘
import pyperclip  # 复制到剪贴板（因为pyautogui不支持输入中文，所以用pyperclip先把中文复制到剪贴板，再用pyautogui按ctrl+v）
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # 定时任务

showroom_id_list = [
    # ------------------------------ =LOVE ------------------------------ #
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
    # ------------------------------ ≠ME ------------------------------ #
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
    # ------------------------------ ≒JOY ------------------------------ #
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
    # ------------------------------ 官方直播间 ------------------------------ #
    "139470",  # =LOVE 官方直播间
    "272301",  # ≠ME 官方直播间
    "402345",  # ≒JOY 官方直播间
    # ------------------------------ 指P ------------------------------ #
    "61774"  # 指原 莉乃
]

showroom_status_list = [1] * len(showroom_id_list)  # 1：未开播，2：已开播

showroom_end_time_list = [0] * len(showroom_id_list)

birthday_list = [
    # -------------------------------------------------- =LOVE -------------------------------------------------- #
    {"name": "大谷 映美里（=LOVE）", "birthday": "03-15"},
    {"name": "大場 花菜（=LOVE）", "birthday": "02-04"},
    {"name": "音嶋 莉沙（=LOVE）", "birthday": "08-11"},
    {"name": "齋藤 樹愛羅（=LOVE）", "birthday": "11-26"},
    {"name": "佐々木 舞香（=LOVE）", "birthday": "01-21"},
    {"name": "髙松 瞳（=LOVE）", "birthday": "01-19"},
    {"name": "瀧脇 笙古（=LOVE）", "birthday": "07-09"},
    {"name": "野口 衣織（=LOVE）", "birthday": "04-26"},
    {"name": "諸橋 沙夏（=LOVE）", "birthday": "08-03"},
    {"name": "山本 杏奈（=LOVE）", "birthday": "11-30"},
    # -------------------------------------------------- ≠ME -------------------------------------------------- #
    {"name": "尾木 波菜（≠ME）", "birthday": "05-08"},
    {"name": "落合 希来里（≠ME）", "birthday": "05-22"},
    {"name": "蟹沢 萌子（≠ME）", "birthday": "10-25"},
    {"name": "河口 夏音（≠ME）", "birthday": "07-29"},
    {"name": "川中子 奈月心（≠ME）", "birthday": "09-26"},
    {"name": "櫻井 もも（≠ME）", "birthday": "04-13"},
    {"name": "菅波 美玲（≠ME）", "birthday": "02-05"},
    {"name": "鈴木 瞳美（≠ME）", "birthday": "04-13"},
    {"name": "谷崎 早耶（≠ME）", "birthday": "10-07"},
    {"name": "冨田 菜々風（≠ME）", "birthday": "07-17"},
    {"name": "永田 詩央里（≠ME）", "birthday": "04-02"},
    {"name": "本田 珠由記（≠ME）", "birthday": "02-27"},
    # -------------------------------------------------- ≒JOY -------------------------------------------------- #
    {"name": "逢田 珠里依（≒JOY）", "birthday": "09-13"},
    {"name": "天野 香乃愛（≒JOY）", "birthday": "01-21"},
    {"name": "市原 愛弓（≒JOY）", "birthday": "08-21"},
    {"name": "江角 怜音（≒JOY）", "birthday": "04-26"},
    {"name": "大信田 美月（≒JOY）", "birthday": "09-27"},
    {"name": "大西 葵（≒JOY）", "birthday": "08-06"},
    {"name": "小澤 愛実（≒JOY）", "birthday": "04-09"},
    {"name": "髙橋 舞（≒JOY）", "birthday": "02-22"},
    {"name": "藤沢 莉子（≒JOY）", "birthday": "01-16"},
    {"name": "村山 結香（≒JOY）", "birthday": "02-15"},
    {"name": "山田 杏佳（≒JOY）", "birthday": "02-02"},
    {"name": "山野 愛月（≒JOY）", "birthday": "10-21"},
    # -------------------------------------------------- 指P -------------------------------------------------- #
    {"name": "指原 莉乃", "birthday": "11-21"}
]

sem = asyncio.Semaphore(10)  # 限制并发请求数为10


async def fetch_showroom_status(session, room_id):
    try:
        # 如果网络不稳定、断网，这里就会报错
        async with session.get(f"https://www.showroom-live.com/api/live/live_info?room_id={room_id}") as response:
            if response.status == 200:
                return await response.json()  # 此处可能出现connection reset错误，原因不明
            else:
                # 访问被拒绝，可能是短时间内访问太多次了
                error_message = f"Failed to fetch data for room {room_id}: {response.status}"
                print(error_message)
                raise Exception(error_message)  # 手动抛出异常，并附带错误信息
    except Exception as e:
        print(f"Exception occurred for room {room_id}: {e}")
        raise


async def fetch_showroom_status_with_sem(session, room_id):
    async with sem:
        return await fetch_showroom_status(session, room_id)


async def check_showroom_status(queue):
    # 当前时间转为日本时间，如果是在凌晨0点到5点之间，就每5分钟才检查一次，因为这是睡觉时间不可能开播，不需要每分钟检查一次
    now = datetime.now(timezone(timedelta(hours=9))).time()
    if time(0, 0) < now < time(5, 0):
        if now.minute % 5 != 0:
            return

    send = ""

    async with aiohttp.ClientSession() as session:
        try:
            tasks = [fetch_showroom_status_with_sem(session, room_id) for room_id in showroom_id_list]
            responses = await asyncio.wait_for(asyncio.gather(*tasks), timeout=10)
        except Exception as e:
            print(f"An error occurred during gathering tasks: {e}")
            return  # 如果fetch_showroom_status中发生异常或此处发生异常，全部忽略掉不处理，让服务器冷静一会儿

        for i, json in enumerate(responses):
            if showroom_status_list[i] == 1 and json["live_status"] == 2:  # 原来没开播，现在开播
                if math.floor(datetime.now().timestamp()) - showroom_end_time_list[i] > 5 * 60:
                    send += f"{json['room_name']}\n▶️ 直播中！\n\n"
                    showroom_status_list[i] = json["live_status"]
                    print(f"{json['room_name']} 已开播")
                else:
                    showroom_status_list[i] = json["live_status"]
                    print(f"{json['room_name']} 疑似断线重连")
            elif showroom_status_list[i] == 2 and json["live_status"] == 1:  # 原来已开播，现在下播
                showroom_status_list[i] = json["live_status"]
                showroom_end_time_list[i] = math.ceil(datetime.now().timestamp())
                print(f"{json['room_name']} 已下播")
            elif showroom_status_list[i] == 2 and json["live_status"] == 2:  # 原来已开播，现在直播中
                print(f"{json['room_name']} 持续直播中……")
            elif showroom_status_list[i] == 1 and json["live_status"] == 1:  # 原来没开播，现在也没开播
                pass
            else:
                print("警告：未知直播状态！")

    if send:
        await queue.put(send)

    print("showroom 最后检查时间：" + datetime.now().strftime("%H:%M:%S"))


async def birthday_reminder(queue):
    send = ""

    # 日本时间：UTC+9
    today = datetime.now(timezone(timedelta(hours=9))).strftime("%m-%d")

    # 可能有多个人同一天生日
    birthday_today = [person["name"] for person in birthday_list if person["birthday"] == today]

    for person in birthday_today:
        send += f"{person}\n🎂 生日快乐！\n{today}\n\n"
        print(f"{person} 生日快乐！")

    if send:
        await queue.put(send)


async def check_network():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.baidu.com") as response:
                return response.status == 200
    except Exception as e:
        print(f"网络检查失败: {e}")
        return False


async def message_consumer(queue):
    while True:
        try:
            if not queue.empty():
                network_status = await check_network()
                if not network_status:
                    print("网络异常！")
                    await asyncio.sleep(1 * 60)
                    raise Exception("网络异常！")
                else:
                    send = await queue.get()
                    if send:
                        send += datetime.now().strftime("%H:%M:%S")
                        pyperclip.copy(send)
                        pyautogui.click(x=2666, y=1777)
                        await asyncio.sleep(0.1)
                        pyautogui.hotkey("ctrl", "v")
                        await asyncio.sleep(0.1)
                        pyautogui.hotkey("enter")
                        print("消息已发送，当前时间：" + datetime.now().strftime("%H:%M:%S"))
                    queue.task_done()
        except Exception as e:
            print(f"发送消息时出现错误: {e}")

        await asyncio.sleep(5)  # 每次暂停5秒，避免频繁轮询


async def main():
    queue = asyncio.Queue()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_showroom_status, "cron", second=0, args=[queue])  # 每分钟0秒执行一次生产者任务
    scheduler.add_job(birthday_reminder, "cron", hour=23, args=[queue])  # 每天晚上11点执行一次生产者任务
    scheduler.start()

    asyncio.create_task(message_consumer(queue))  # 这里不能使用await，因为是无限循环，会一直卡在这里

    await birthday_reminder(queue)

    await asyncio.Future()  # 保持 main() 持续运行，让定时器等持续运行


if __name__ == "__main__":
    asyncio.run(main())
