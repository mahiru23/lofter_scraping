#!/usr/bin/env python3
import requests

url = "https://www.lofter.com/dwr/call/plaincall/PostBean.getFavTrackItem.dwr"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Content-Type": "text/plain",
    "Origin": "https://www.lofter.com",
    "Referer": "https://www.lofter.com/like",
}

# 从浏览器复制完整的 Cookie 字符串粘贴进来
cookies = {
    "LOFTER_SESS": "BGWW9bGr3lGwztvMvh-Nj7-nHcC8qe2nvrBkOP4Uqune0e2QFN2msgMu3xmhfctOQpAo8AQfNFaYduxQzFsrbeZaxAY7q7veC7CqZhIUcLCjVXY_Fh47vnOx8dzHN8Gu",
    # 其他关键 Cookie 项也可以加进来，例如 JSESSIONID 等
}

# POST 请求的请求体内容（从 Chrome DevTools 的 Request Payload 中复制）
data = """callCount=1
scriptSessionId=${scriptSessionId}187
httpSessionId=
c0-scriptName=ArchiveBean
c0-methodName=getArchivePostByTime
c0-id=0
c0-param0=boolean:false
c0-param1=number:537665661
c0-param2=number:1743850365330
c0-param3=number:500
c0-param4=boolean:false
batchId=873961"""

response = requests.post(url, headers=headers, cookies=cookies, data=data)

print(response.text)
