from bs4 import BeautifulSoup
import requests # 抓取页面

def fetch_chapter(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Referer': url
    }

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"请求失败，状态码: {r.status_code}")
        return None, None

    demo = r.text
    soup = BeautifulSoup(demo, 'html.parser')

    # 找到章节名
    chapter_title = soup.find('div', class_='booktitle').h1.text + '\n\n'

    # 找到内容
    content_div = soup.find('div', class_='content', id='chaptercontent')
    content = content_div.get_text(separator="\n\n").strip()

    # 找到下一章的链接
    next_chapter_link = soup.find('a', rel='next')
    next_chapter_url = None
    if next_chapter_link:
        next_chapter_url = next_chapter_link['href']
        # 拼接完整URL
        if next_chapter_url.startswith('/'):
            next_chapter_url = 'https://www.fd80s.com' + next_chapter_url

    return (chapter_title, content, next_chapter_url)

novel_content = ""
start_url = 'https://www.fd80s.com/254/254766/2301280.html'
j = 0
while start_url:
    title, content, start_url = fetch_chapter(start_url)
    if title and content:
        novel_content += title
        novel_content += content

    else:
        print(start_url)
    j+=1
    print(j)


# 保存整本小说到txt文件
with open('xxx.txt', 'w', encoding='utf-8') as file:
    file.write(novel_content)
