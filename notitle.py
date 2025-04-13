#!/usr/bin/env python3

import requests
import time
import os
from datetime import datetime
from bs4 import BeautifulSoup
import re
import unicodedata



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



def extract_urls_from_log(file_path):
    # 用于匹配指定格式的 URL：开头为 [no title error]，后接一个 https://xxx.lofter.com/post/xxx
    pattern = r'\[no title error\]\s+(https://[a-zA-Z0-9\-]+\.lofter\.com/post/[a-zA-Z0-9_]+)'

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用 findall 提取所有符合格式的链接
    urls = re.findall(pattern, content)
    return urls

# 示例用法
log_file = 'save.log'
urls = extract_urls_from_log(log_file)
print(len(urls))



# 新建文件夹
folder_prefix = f"archive"
folder = f"{folder_prefix}/notitle"
os.makedirs(folder, exist_ok=True) #已存在则跳过

for url in urls:
    while True:
        ret = fetch_and_save(url, folder)
        if ret:
            break
        time.sleep(1)


