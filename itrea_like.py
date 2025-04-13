#!/usr/bin/python3

import requests
import time
import os
from datetime import datetime

# 设置请求信息
url = "https://www.lofter.com/dwr/call/plaincall/PostBean.getFavTrackItem.dwr"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Content-Type": "text/plain",
    "Origin": "https://www.lofter.com",
    "Referer": "https://www.lofter.com/like",
}

# 替换为你自己的完整 cookie 信息
cookies = {
    "LOFTER_SESS": "BGWW9bGr3lGwztvMvh-Nj7-nHcC8qe2nvrBkOP4Uqune0e2QFN2msgMu3xmhfctOQpAo8AQfNFaYduxQzFsrbeZaxAY7q7veC7CqZhIUcLCjVXY_Fh47vnOx8dzHN8Gu",
}

# 设置变量
like_sum = 584
step = 40  # 每次最多请求40条
timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
folder = f"fav-{timestamp}"

# 创建保存目录
os.makedirs(folder, exist_ok=True)

# 循环请求数据
for start in range(1, like_sum + 1, step):
    end = min(start + step - 1, like_sum)
    print(f"请求点赞 {start} 到 {end} ...")

    data = f"""callCount=1
scriptSessionId=${{scriptSessionId}}190
httpSessionId=
c0-scriptName=PostBean
c0-methodName=getFavTrackItem
c0-id=0
c0-param0=number:{step}
c0-param1=number:{start}
batchId=0"""

    try:
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        response.raise_for_status()
        filename = f"{folder}/like-{start}-{end}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"已保存至 {filename}")
    except Exception as e:
        print(f"请求失败：{e}")

    # 等待 5 秒，避免触发风控
    time.sleep(5)

print("所有请求完成 ✅")
