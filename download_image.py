import os
import json
import time
import requests
from datetime import datetime

def download_image(url, file_path):
    response = requests.get(url)  # 发送GET请求获取响应对象
    with open(file_path, 'wb') as f:  # 以二进制写入模式打开文件
        f.write(response.content)  # 将响应内容写入文件

def read_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        return list(set(data))
    else:
        return []

def write_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

def main(i):
    now = datetime.now()
    date = now.date()
    folder = str(date)
    if not os.path.exists(folder):
        os.makedirs(folder)

    image_names = read_json('img_name.json')
    fileurls = read_json('img_url.json')
    downloaded_names = []

    while i > 0:
        time.sleep(1)
        url = 'https://www.dmoe.cc/random.php?return=json'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Referer': 'https://www.dmoe.cc',
        }
        turl = requests.get(url, headers=headers).json()
        url = turl['imgurl']
        filename = url.split("/")[-1]
       
        if filename in image_names:
            continue

        image_names.append(filename)
        fileurls.append('https://cdn.jsdelivr.net/gh/Codebglh/img_warehouse/'+folder+'/'+filename)
        downloaded_names.append('https://cdn.jsdelivr.net/gh/Codebglh/img_warehouse/'+folder+'/'+filename)

        file_path = os.path.join(folder, filename)
        download_image(url, file_path)

        i -= 1

    write_json('img_name.json', image_names)
    write_json('img_url.json', fileurls)

    imgname_filename = os.path.join(folder, 'img_name.json')
    write_json(imgname_filename, downloaded_names)

    md_filename = 'README.md'
    md_path = os.path.join(folder, md_filename)
    with open(md_path, 'w') as f:
        f.write('# Downloaded Images\n\n')
        f.writelines([f'![]({name})\n```\n{name}\n```\n' for name in downloaded_names])



if __name__ == '__main__':
    main(100)
