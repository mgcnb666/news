import os
import datetime
import time
import random
import requests
from bs4 import BeautifulSoup

# 设置你的 GitHub 仓库路径
repo_path = '/root/news/newss'  # 根据实际情况修改
os.chdir(repo_path)

while True:
    # 获取当前日期和时间
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.datetime.now().strftime('%H:%M:%S')

    # 网站 URL（例如：BBC 新闻）
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析网页
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找新闻标题和链接
        articles = soup.find_all('a', class_='gs-c-promo-heading')  # 更新为正确的选择器

        # 创建或更新文件
        file_name = f'news_{current_date}.txt'
        with open(file_name, 'w') as f:
            f.write(f'News on {current_date} at {current_time}\n\n')
            for article in articles[:10]:  # 只取前10条
                title = article.find('h3').get_text() if article.find('h3') else 'No title'
                link = article['href']
                if not link.startswith('http'):
                    link = 'https://www.bbc.com' + link
                f.write(f'Title: {title}\nURL: {link}\n\n')

        # Git 操作
        try:
            # 检查是否有未完成的合并
            if os.path.exists('.git/MERGE_HEAD'):
                print("There is an unfinished merge. Please resolve it before running this script again.")
                break  # 或者选择手动处理

            os.system('git config pull.rebase false')  # 使用合并策略
            os.system('git pull origin main')  # 拉取远程更改
            os.system('git add .')
            commit_message = f"Daily news contribution on {current_date} at {current_time}"
            os.system(f'git commit -m "{commit_message}"')  # 自动提交信息
            os.system('git push git@github.com:mgcnb666/news.git')  # 替换为您的 SSH URL
        except Exception as e:
            print(f"Error during Git operations: {e}")

        # 生成随机时间间隔（12到13小时之间的秒数）
        wait_time = random.randint(43200, 46800)  # 43200秒到46800秒
        print(f"Waiting for {wait_time // 3600} hours before the next update...")
        time.sleep(wait_time)
    else:
        print("Error fetching news:", response.status_code)
        time.sleep(3600)  # 如果出错，等待1小时再重试
