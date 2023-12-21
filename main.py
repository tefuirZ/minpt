#!/usr/bin/python3
# -*- coding: utf-8 -*-
import bs4
import requests
import os
import lxml
import re
import configparser
from urllib.parse import urlparse, parse_qs, urlencode

# 检查配置文件是否存在，如果不存在，则创建一个默认配置文件
CONFIG_FILE_PATH = 'config.ini'
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
config.read(CONFIG_FILE_PATH)

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

url_half = re.search(r'(https?://[^/]+)/', site_url).group(1)
referer = config.get(runsite, 'referer', fallback='')
host = re.search(r'://([^/]+)/', site_url).group(1)

monitor_path = config.get(runsite, 'monitor_path', fallback=r'F:\\1\\')
user_agent = config.get(runsite, 'user_agent', fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76')
download_times = config.getint(runsite, 'download_times', fallback=1)
site_cookie = f"c_lang; {site_cookie}"
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





    is_gazelle = False
    is_encrypted = False
    # 下载种子文件



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
            res = s.get(url, headers=my_headers)
        else:
            res = s.get(url)
        return res


    class Torrents():


        def __init__(self, torrent):
            self.torrent = torrent

        def __str__(self):
            return '{}_{}.torrent'.format(site_name, self.torrent[1])

        def download(self):
            torrent_id = self.torrent[1]
            download_url = f"https://{host}/download.php?id={torrent_id}"
            res = requests_check_headers(download_url)

            print('\n\nDownloading ' + self.__str__())
            try:
                print('正在下载。。。。。')
                with open(monitor_path + self.__str__(), 'wb') as f:
                    f.write(res.content)
            except Exception as e:
                print(f'Error writing torrent file: {e}')

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
        if os.path.isfile(monitor_path + "downloaded_list.log") == False:
            with open(monitor_path + "downloaded_list.log", 'w') as f:
                f.write("已经下载的种子id:\n")

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
                    Torrents(torrent).download()
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
                    Torrents(torrent).download()
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
    my_headers = get_my_headers(my_headers={})

    if not is_gazelle:
        if not is_encrypted:
            task = NexusPage(
                torrents_class_name)
            task = NexusPage(
                torrents_class_name)
            task_list = task.find_free()
            download_free(torrents_amount, task_list, monitor_path)
        else:
            task = NexusPage(
                HDC_torrents_class_name)
            task = NexusPage(
                HDC_torrents_class_name)
            task_list = task.find_free(free_tag, free_tag2)
            download_encrypted_free(torrents_amount, task_list, monitor_path, HDC_download_class_name)
    #####
    else:
        task = GazellePage(
            DIC_torrents_class_name)
        task = GazellePage(
            DIC_torrents_class_name)
        task_list = task.find_free(DIC_free_tag)
        download_free(torrents_amount, task_list, monitor_path)
print('所有种子下载完成')
