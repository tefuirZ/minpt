
# PT站点批量下载种子脚本

## 功能实现

本脚本能够批量下载站点按照你自己排序的页面的全部种子文件。主要功能包括：

- 多站点配置
- 可设置循环次数进行种子下载，下载种子个数取决于你站点设置的页面中个数乘以循环次数，默认为1
- 自动配置浏览器代理、请求头等信息
- 多站点根据配置文件中的站点名称对种子进行命名

## 食用方法
### 一、源码运行
1. 机器安装Python3.7以上环境
2. 使用 `pip install -r requirements.txt` 安装所需模块
3. 修改配置文件 `config.ini` 中的信息
4. 环境配置完之后 运行`python3.x mian.py` 其中`python3.x`根据你安装的python环境更改



### 二、docker运行
```
docker run -d \
  --name minpt \
  -v /your/path/config.ini:/app/config.ini \
  -v /yourpath:/torrent \
itefuir/minpt:latest

```
使用docker运行时注意目录的权限，如果目录不存在，一定一定一定要先将目录创建并且给777权限否则会看不到种子文件。

配置文件示例：

```
[DEFAULT]
runsite = pttime

[pttime]
site_name = pttime
site_url = pttime.xxx/torrents.php?inclbookmarked=0&incldead=1&spstate=0&&sort=5&type=asc&page=1
site_cookie = cookie
monitor_path = F:\\1\\
download_times = 1
```

- `runsite`: 选择要运行的站点名字
- `site_name`: 站点名称
- `site_url`: 要下载的页面
- `site_cookie`: 站点小饼干
- `monitor_path`: 种子存储位置
- `download_times`: 循环次数，可以理解为下载的页码

种子批量下载完成后，你可以使用种子下载工具自动监控种子文件夹进行下载种子，这样批量下载小文件会更加方便。

保最多的电子书，做魔力大咖（bushi）。


这个脚本有些地方是使用ChatGPT来修改的，原脚本出处已经忘了。望大伙将就用~ 有问题可以提~
