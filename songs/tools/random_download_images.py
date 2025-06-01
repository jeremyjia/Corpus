import requests
import random
import os
import argparse
from urllib.parse import urlparse
from pathlib import Path

def get_github_repo_contents(repo_url):
    """获取GitHub仓库的内容列表"""    
    # 发送请求
    response = requests.get(repo_url)
    if response.status_code != 200:
        raise Exception(f"获取仓库内容失败: {response.status_code} {response.text}")
    
    return response.json()

def filter_image_files(items):
    """筛选出图片文件"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    return [item for item in items if Path(item['name']).suffix.lower() in image_extensions]

def download_images(image_items, count, output_dir='.', list_file='downloaded_images.txt'):
    """
    随机下载指定数量的图片并记录到文件
    
    参数:
        image_items: 图片项列表
        count: 要下载的数量
        output_dir: 输出目录
        list_file: 记录下载文件名的文本文件
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 随机选择图片
    selected_images = random.sample(image_items, min(count, len(image_items)))
    downloaded_files = []
    
    # 下载图片
    for i, image in enumerate(selected_images):
        download_url = image['download_url']
        original_name = image['name']
        file_ext = Path(original_name).suffix
        new_name = f"frame_{i}{file_ext}"
        file_path = os.path.join(output_dir, new_name)
        
        # 检查文件是否已存在
        if os.path.exists(file_path):
            print(f"文件已存在，跳过下载: {file_path}")
            downloaded_files.append(f'{new_name}')
            continue
        
        try:
            response = requests.get(download_url)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"已下载: {file_path}")
                downloaded_files.append(f'{new_name}')
            else:
                print(f"下载失败 {download_url}: {response.status_code}")
        except Exception as e:
            print(f"下载时出错 {download_url}: {e}")
    
    # 将下载的文件名写入文本文件
    if downloaded_files:
        try:
            list_path = os.path.join(output_dir, list_file)
            with open(list_path, 'w') as f:
                #f.write(','.join(downloaded_files))
                index = 0
                while index < len(downloaded_files):
                    if(index == 0 or index==len(downloaded_files)):
                        f.write(downloaded_files[index])
                    else:
                        f.write("\",\""+downloaded_files[index])
                    index+=1
            print(f"已记录下载文件列表到: {list_path}")
        except Exception as e:
            print(f"写入文件列表时出错: {e}")

def main():
    parser = argparse.ArgumentParser(description='从GitHub仓库随机下载图片')
    parser.add_argument('-i', '--input', help='GitHub仓库URL')
    parser.add_argument('-c', '--count', type=int, default=2, help='要下载的图片数量')
    parser.add_argument('-d', '--dir', default='.', help='输出目录')
    parser.add_argument('-o', '--output', default='downloaded_images.txt', help='记录下载文件名的文本文件')
    
    args = parser.parse_args()

    in_text = args.input
    prefix, repourl = in_text.split("-", 1) #string-a cat
    
    try:
        # 获取仓库内容
        contents = get_github_repo_contents(repourl)
        
        # 筛选图片文件
        image_files = filter_image_files(contents)
        
        if not image_files:
            print("在仓库中未找到图片文件")
            return
        
        print(f"找到 {len(image_files)} 张图片")
        
        # 下载图片
        download_images(image_files, args.count, args.dir, args.output)
        
        print(f"下载完成，共下载 {min(args.count, len(image_files))} 张图片到目录: {args.output}")
        
    except Exception as e:
        print(f"程序执行出错: {e}")

if __name__ == "__main__":
    #python3 random_download_images.py -i "string-https://api.github.com/repos/jeremyjia/Corpus/contents/songs/pic/szbf" -c 2 -o 1.txt

    main()