#!/usr/bin/python3
# -*- coding: utf-8 -*-
import bs4
import requests
import os
import lxml
import re
import configparser
from urllib.parse import urlparse, parse_qs, urlencode
import time
import random

DEFAULT_REST_INTERVAL = 30  # 默认休息时间为30-60S
DEFAULT_TORRENTS_PER_BATCH = 30  # 默认每批下载30个种子


# 检查配置文件是否存在，如果不存在，则创建一个默认配置文件
CONFIG_FILE_PATH = os.getenv('CONFIG_FILE_PATH', 'config.ini')
if not os.path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, 'w') as config_file:
        config_file.write("""[DEFAULT]
runsite = hhanclub

[hhanclub]
site_name = YourSiteName
site_url = YourSiteURL
site_cookie = YourSiteCookie
referer = YourReferer
monitor_path = F:\\1\\
user_agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76
download_times = 1
""")

# 读取配置文件
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH, encoding='utf-8')

# 读取 runsite 配置项，用于选择要运行的站点
runsite = config.get('DEFAULT', 'runsite', fallback='hhanclub')
# 检查 runsite 是否在配置文件中存在
if runsite not in config:
    print(f"Error: The specified site '{runsite}' is not found in the configuration file.")
    exit()

# 使用选定的站点配置
site_name = config.get(runsite, 'site_name')
site_url = config.get(runsite, 'site_url')
site_cookie = config.get(runsite, 'site_cookie', raw=True)
passkey = config.get(runsite, 'passkey', fallback='')
url_half = re.search(r'(https?://[^/]+)/', site_url).group(1)
referer = config.get(runsite, 'referer', fallback='')
host = re.search(r'://([^/]+)/', site_url).group(1)
operation_type = config.getint(runsite, 'operation_type', fallback=1)
monitor_path = config.get(runsite, 'monitor_path', fallback=r'F:\\1\\')
user_agent = config.get(runsite, 'user_agent', fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76')
download_times = config.getint(runsite, 'download_times', fallback=1)
site_cookie = f"c_lang_folder=cht; {site_cookie}"
rest_interval_low = config.getint(runsite, 'rest_interval_low', fallback=DEFAULT_REST_INTERVAL)
rest_interval_high = config.getint(runsite, 'rest_interval_high', fallback=2 * DEFAULT_REST_INTERVAL)
torrents_per_batch = config.getint(runsite, 'torrents_per_batch', fallback=DEFAULT_TORRENTS_PER_BATCH)
parsed_url = urlparse(site_url)
query_params = parse_qs(parsed_url.query)



if 'page' not in query_params:
    # 将&page=1添加到URL
    site_url = site_url + '&page=1'
# 循环下载

for _ in range(download_times):
    # 获取当前页面编号
    match = re.search(r'&page=(\d+)', site_url)
    current_page = int(match.group(1)) if match else 1

    # 递增页面编号
    new_page = current_page + 1

    # 更新 site_url
    site_url = re.sub(r'&page=\d+', f'&page={new_page}', site_url)

    # 输出调试语句
    print(f'\n下一批下载的更新URL：{site_url}')
    # 随机生成休息时间在指定范围内
    rest_interval = random.randint(rest_interval_low, rest_interval_high)
    print(f'随机休息时间: {rest_interval} 秒')





    is_gazelle = False
    is_encrypted = False


    upgrade_insecure_requests = ''
    dnt = ''
    accept_language = ''
    accept_encoding = ''
    accept = ''
    cache_control = ''
    content_length = ''
    content_type = ''
    origin = ''
    accept_encoding = ''

    torrents_amount = 0
    colspan = '3'
    free_tag = 'torrent-manage'
    free_tag2 = 'pro_free2up'
    DIC_free_tag = 'torrent_label tooltip tl_free'

    torrents_class_name = '.torrentname'
    HDC_torrents_class_name = '.t_name'
    DIC_torrents_class_name = '.td_info'

    download_class_name = '.download'
    HDC_download_class_name = '.torrentdown_button'

    cookie_dict = {"cookie": site_cookie}
    s = requests.Session()
    s.cookies.update(cookie_dict)
    pattern = r'id=(\d+)'


    def get_my_headers(my_headers={}):

        if user_agent:
            my_headers['User-Agent'] = user_agent
        if referer:
            my_headers['Referer'] = referer
        if host:
            my_headers['Host'] = host
        if accept:
            my_headers['accept'] = accept
        if accept_language:
            my_headers['accept-language'] = accept_language
        if accept_encoding:
            my_headers['accept-encoding'] = accept_encoding
        if origin:
            my_headers['origin'] = origin
        if dnt:
            my_headers['dnt'] = dnt
        if upgrade_insecure_requests:
            my_headers['upgrade-insecure-requests'] = upgrade_insecure_requests
        if cache_control:
            my_headers['cache-control'] = cache_control
        if content_length:
            my_headers['content-length'] = content_length
        if content_type:
            my_headers['content-type'] = content_type

        return my_headers


    def requests_check_headers(url):
        if user_agent or referer or host:
            res = s.get(url, headers=my_headers, allow_redirects=True)
        else:
            res = s.get(url)
        return res


    class Torrents():


        def __init__(self, torrent):
            self.torrent = torrent

        def __str__(self):
            return '{}_{}.torrent'.format(site_name, self.torrent[1])

        def download(self):
            # 保存下载链接
            torrent_id = self.torrent[1]
            download_url = f"https://{host}/download.php?id={torrent_id}"

            # 如果有 passkey，则在下载链接中包含 passkey
            if passkey:
                download_url += f"&passkey={passkey}"

            print(f"Saving link for torrent: {self.__str__()} - {download_url}")

            # 根据 operation_type 决定下载方式
            if operation_type == 1:
                self._download_torrent_file()
            elif operation_type == 2:
                # 将下载链接写入站点名称的文件中
                links_file_path = os.path.join(monitor_path, f"{site_name}_种子连接.txt")
                with open(links_file_path, 'a') as links_file:
                    links_file.write(f" {download_url}\n")
                    print(f"正在写入种子连接 {download_url}")
            else:
                print("Error: Invalid operation_type specified in the configuration.")

        def _download_torrent_file(self):
            # 只有在下载文件的分支中实际下载种子文件
            download_url = f"https://{host}/download.php?id={self.torrent[1]}"

            # 如果有 passkey，则在下载链接中包含 passkey
            if passkey:
                download_url += f"&passkey={passkey}"

            res = requests_check_headers(download_url)

            print('\n\nDownloading ' + self.__str__())
            try:
                print('正在下载。。。。。')
                print({download_url})
                with open(monitor_path + self.__str__(), 'wb') as f:
                    f.write(res.content)
            except Exception as e:
                print(f'种子写入指定路径失败，请检查路径权限: {e}')

        def encrypted_download(self, download_class_name):
            download_page = url_half + self.torrent[2]
            if self.torrent[0]:
                response = requests_check_headers(download_page)
                soup = bs4.BeautifulSoup(response.text, 'lxml')
                down_url_last = soup.select_one(download_class_name)[
                    'href']
                down_url = url_half + down_url_last
                res = requests_check_headers(down_url)
                print('\n\n注意:下载中字大小！！！！ ')
                try:
                    print('下载中' + self.__str__())
                except:
                    print('Cannot print the torrent name.')
                try:
                    print('写入中。。。。。')
                    with open(monitor_path + self.__str__(), 'wb') as f:
                        f.write(res.content)
                except:
                    print('无法写入目录，请检查目录是否正确、是否有权限访问目录。')
            else:
                pass


    class NexusPage():

        def __init__(self, torrents_class_name):
            self.torrents_list = []
            self.processed_list = []
            self.torrents_class_name = torrents_class_name

            res = requests_check_headers(site_url)
            soup = bs4.BeautifulSoup(res.text, 'lxml')
            self.processed_list = soup.select(self.torrents_class_name)
#            print('\n\nThe website shows: ')
#            try:
#                print(str(soup))
#            except:
#                print('Cannot print soup')
#            print('\n\nThe torrents informations(processed_list) shows below: ')
#           try:
#                print(self.processed_list)
#            except:
#                print('Cannot print processed_list')


        def __str__(self):
            return self.processed_list

        def find_free(self):
            free_state = []
            for entry in self.processed_list:
                details = entry.a['href']
                torrent_id = re.search(pattern, details).group(1)
                last_download_url = 'NULL'
                for subentry in entry.select('.embedded'):
                    if 'href="download.php?' in str(subentry):
                        last_download_url = subentry.a['href']
                free_state.append((True, torrent_id, details, last_download_url))

            return free_state


    #####
    class GazellePage():

        def __init__(self, torrents_class_name):
            self.torrents_list = []
            self.processed_list = []
            self.torrents_class_name = torrents_class_name

            res = requests_check_headers(site_url)
            soup = bs4.BeautifulSoup(res.text, 'lxml')
            self.torrents_list = soup.select(self.torrents_class_name)

            for entry in self.torrents_list:
                if entry['colspan'] == colspan:
                    self.processed_list.append(entry)
#            print('\n\nThe website shows: ')
#            try:
#                print(str(soup))
#            except:
#                print('Cannot print soup')
#            print('\n\nThe torrents informations(processed_list) shows below: ')
#            try:
#                print(self.processed_list)
#            except:
#                print('Cannot print processed_list')

        def __str__(self):
            return self.processed_list

        def find_free(self, free_tag, free_tag2=''):
            free_state = []
            for entry in self.processed_list:
                last_download_url = entry.a['href']
                torrent_id = re.search(pattern, last_download_url).group(1)
                details = 'torrents.php?id=' + torrent_id

                if entry.find(class_=free_tag) or entry.find(class_=free_tag2):
                    free_state.append((True, torrent_id, details, last_download_url))
                else:
                    free_state.append((False, torrent_id, details, last_download_url))
            print("\n\nThe torrents' free state tuples list shows below: ")
            try:
                print(free_state)
            except:
                print('Cannot print the free_tuple_list')
            return free_state


    #####
    def download_free(torrents_amount, task_list, monitor_path):
        global rest_interval  # 声明 rest_interval 为全局变量
        downloaded_count = 0  # 初始化下载计数器
        if os.path.isfile(monitor_path + "downloaded_list.log") == False:
            with open(monitor_path + "downloaded_list.log", 'w') as f:
                f.write("已经下载的种子id:\n")

        for torrent in task_list:
            torrent_name = str(Torrents(torrent))
            with open(monitor_path + "downloaded_list.log", 'r') as f:
                downloaded = f.read()
                if torrent_name in downloaded:
                    continue
            with open(monitor_path + "downloaded_list.log", 'a') as f:
                f.write(torrent_name + '\n')  # 修复了写入下载列表时缺少换行符的问题

            if os.path.isfile(monitor_path + torrent_name) == False:
                Torrents(torrent).download()
                downloaded_count += 1  # 增加下载计数
                if downloaded_count >= torrents_per_batch:  # 当达到批次下载数量时
                    print(f"已下载 {downloaded_count} 个种子，休息 {rest_interval} 秒...")
                    time.sleep(rest_interval)  # 暂停执行指定的秒数
                    rest_interval = random.randint(rest_interval_low, rest_interval_high)  # 重新生成随机休息时间
                    downloaded_count = 0  # 重置下载计数器
            else:
                continue


    #####
    def download_encrypted_free(torrents_amount, task_list, monitor_path, download_class_name):
        if os.path.isfile(monitor_path + "downloaded_list.log") == False:
            with open(monitor_path + "downloaded_list.log", 'w') as f:
                f.write("A list shows the torrents have been downloaded:\n")

        if not torrents_amount:
            for torrent in task_list:
                torrent_name = str(Torrents(torrent))

                with open(monitor_path + "downloaded_list.log", 'r') as f:
                    downloaded = f.read()
                    if torrent_name in downloaded:
                        continue
                with open(monitor_path + "downloaded_list.log", 'a') as f:
                    f.write(torrent_name)

                if os.path.isfile(monitor_path + torrent_name) == False:
                    Torrents(torrent).encrypted_download(download_class_name)
                else:
                    continue
        else:
            for torrent in task_list[0:torrents_amount:1]:
                torrent_name = str(Torrents(torrent))

                with open(monitor_path + "downloaded_list.log", 'r') as f:
                    downloaded = f.read()
                    if torrent_name in downloaded:
                        continue
                with open(monitor_path + "downloaded_list.log", 'a') as f:
                    f.write(torrent_name)

                if os.path.isfile(monitor_path + torrent_name) == False:
                    Torrents(torrent).encrypted_download(download_class_name)
                else:
                    continue



    #####
    my_headers = get_my_headers(my_headers={'User-Agent': ''})

    if not is_gazelle:
        if not is_encrypted:
            task = NexusPage(torrents_class_name)
            task_list = task.find_free()
            download_free(torrents_amount, task_list, monitor_path)
        else:
            task = NexusPage(HDC_torrents_class_name)
            task_list = task.find_free(free_tag, free_tag2)
            download_encrypted_free(torrents_amount, task_list, monitor_path, HDC_download_class_name)
    else:
        task = GazellePage(DIC_torrents_class_name)
        task_list = task.find_free(DIC_free_tag)
        download_free(torrents_amount, task_list, monitor_path)
    # 根据 operation_type 决定下载方式
    if operation_type == 1:
        # 下载并保存种子文件
        for torrent in task_list:
            Torrents(torrent).download()
    elif operation_type == 2:
        # 将下载链接写入文件
        with open(monitor_path + "downloaded_links.txt", 'a') as links_file:
            for torrent in task_list:
                torrent_name = str(Torrents(torrent))
                download_link = f"https://{host}/download.php?id={torrent[1]}&passkey={passkey}&https=1"
                links_file.write(f"{torrent_name}: {download_link}\n")
                print(f"Saving link for torrent: {torrent_name}")
    else:
        print("Error: Invalid operation_type specified in the configuration.")

    # 随机生成休息时间在指定范围内
    rest_interval = random.randint(rest_interval_low, rest_interval_high)
    print(f'随机休息时间: {rest_interval} 秒')

    # 休息指定时间
    time.sleep(rest_interval)

    # 检查当前页面是否还有未下载的种子，如果有则继续下载当前页面的剩余种子
    remaining_torrents = len(task_list) - torrents_per_batch
    if remaining_torrents > 0:
        print(f"当前页面还有 {remaining_torrents} 个种子未下载，继续下载...")
    else:
        print("当前页面的种子已全部下载完毕，准备进入下一批页面...")
print('全部种子下载完成')
