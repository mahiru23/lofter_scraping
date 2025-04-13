#!/usr/bin/env python3

import requests
import time
import os
from datetime import datetime
from bs4 import BeautifulSoup
import re
import unicodedata

# c0_param1_value: user_id，去查询作者唯一id
# 作用是遍历某个作者自c0_param2（毫秒级时间戳）之后的所有作品（此处设置500为最大值）
def fetch_data(user_id):
    # 动态获取当前时间减去1小时的毫秒级时间戳
    current_time = datetime.now()
    timestamp_ms = int(current_time.timestamp() * 1000)

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

    # POST 请求的请求体内容，c0-param2 设置为动态计算的时间戳
    data = f"""callCount=1
scriptSessionId=${{scriptSessionId}}187
httpSessionId=
c0-scriptName=ArchiveBean
c0-methodName=getArchivePostByTime
c0-id=0
c0-param0=boolean:false
c0-param1=number:{user_id}
c0-param2=number:{timestamp_ms}
c0-param3=number:500
c0-param4=boolean:false
batchId=873961"""

    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    return response

# 从response text中提取permalink
def extract_permalink(response_text):
    # Regular expression to match permalink values
    permalink_pattern = r's\d+\.permalink="([^"]+)"'
    
    # Find all occurrences of the permalink pattern
    permalinks = re.findall(permalink_pattern, response_text)
    
    return permalinks

# 从单个url中提取html并保存
# e.g. url = 'https://zhenrongyiya.lofter.com/post/200c207d_2ba2a832d'
def fetch_and_save(url, folder):
    # 设置请求头，包括cookie和其他相关信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6',
        'Cookie': 'usertrack=CpiybWfEPewtJwCAtSEVAg==; JSESSIONID-WLF-XXD=fe0978cbea8b16bf4eb46f4f9c82db5ca935872302f562ddfce3f410b9242a348a68f771cd1eb890a7d755e25384f03217d99241969fe53baf1f8736746022da19023f7fa9733833a620400b558e8026dce34c492f72e8b277b4ba70cebd55cbfcd5b22d77c61f4781bc954d36ee7e25ec6a50a81b7c7723a07c33757867cd3fa0635a51; LOFTER_SESS=BGWW9bGr3lGwztvMvh-Nj7-nHcC8qe2nvrBkOP4Uqune0e2QFN2msgMu3xmhfctOQpAo8AQfNFaYduxQzFsrbeZaxAY7q7veC7CqZhIUcLCjVXY_Fh47vnOx8dzHN8Gu; NETEASE_WDA_UID=529027315#|#1527692750909; regtoken=2000; reglogin_isLoginFlag=1; __LOFTER_TRACE_UID=EC354CA00C11496EB0923F4A8B9614AE#529027315#3; reglogin_isLoginFlag=1; hb_MA-BFD7-963BF6846668_source=sudixun.lofter.com; NTESwebSI=B7DB2453BDEC11324B274DF70056C3F5.lofter-webapp-web-old-docker-lftpro-3-3nhsm-9past-59967479wvd6b-8080'
    }

    # 发送GET请求
    response = requests.get(url, headers=headers)

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取<title>标签中的内容
    title = ""
    title_tag = soup.title
    if title_tag and title_tag.string:
        title = title_tag.string.strip()
    else:
        print("[no title error] ", url, ", title_tag: ", title_tag)
        return False

    # 去掉非法字符（如文件名中的特殊字符）
    title = ''.join(ch for ch in title if ch not in ('\x00',) and unicodedata.category(ch)[0] != 'C')
    title = re.sub(r'[\\/*?:"<>|]', "", title)

    # 检测文件是否存在
    file_path = os.path.join(folder, f"{title}.txt")
    if os.path.exists(file_path):
        print(f"⏭️ 已存在，跳过保存：{file_path}")
        return True

    # 将返回内容存到以title为文件名的txt文件
    with open(f'{folder}/{title}.txt', 'w', encoding='utf-8') as file:
        file.write(response.text)
    return True

# 保存单个user的archive
# user_id: 537665661
# user_name: "zhenrongyiya"
def get_one_user_archive(user_id, base_url):
    # 新建文件夹
    folder_prefix = f"archive"
    os.makedirs(folder_prefix, exist_ok=True) #已存在则跳过
    folder = f"{folder_prefix}/{user_id}"
    os.makedirs(folder, exist_ok=True) #已存在则跳过

    # get并提取该作者所有permalinks
    # e.g. 200c207d_2ba2a832d
    response = fetch_data(user_id)
    permalinks = extract_permalink(response.text)
    print(permalinks)

    # 基础URL前缀
    # base_url = f"https://{user_name}.lofter.com/post/"
    for permalink in permalinks:
        full_url = base_url + permalink
        print(full_url)
        while True:
            ret = fetch_and_save(full_url, folder)
            if ret:
                break
            # 等待 1 秒，避免触发风控
            time.sleep(1)


def extract_blog_info_from_dir(folder):
    pair_dict = {}
    
    # 精准匹配该格式的正则
    pattern = re.compile(
        r'blogId=(\d+);[^;]*;[^;]*blogPageUrl="(https://[^/]+\.lofter\.com/post/)[^"]*"'
    )

    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if not os.path.isfile(filepath) or not filename.endswith(".txt"):
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

            matches = pattern.findall(content)
            for blog_id, base_url in matches:
                pair_dict[int(blog_id)] = base_url  # 保证 blogId 是数字

    #for blog_id, base_url in pair_dict.items():
    #    print(blog_id, "->", base_url)
    return pair_dict




pair_dict = extract_blog_info_from_dir("fav-20250405-173918")

for user_id, base_url in pair_dict.items():
   get_one_user_archive(user_id, base_url)

#get_one_user_archive(1286422124, "https://zhexuejiashidifu.lofter.com/post/")

print("archive over")




