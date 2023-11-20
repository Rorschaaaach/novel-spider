# 导入bs4库
from bs4 import BeautifulSoup
import requests # 抓取页面
import time

novel_content = ""
j = 0
for i in range(1, 22):
    r = requests.get('http://www.fd80.com/bookindex/132711644/' + str(i) + '.html') # Demo网址
    demo = r.text  # 抓取的数据

    # 解析HTML页面
    soup = BeautifulSoup(demo, 'html.parser')  # 抓取的页面数据；bs4的解析器
    for li_tag in soup.find_all('li'):
        chapter_name = li_tag.a.get_text(strip=True)
        href_value = li_tag.a['href']
        
        # 获取章节id
        html_code = href_value.split('/')[-1].split('.')[0]
        
        chapter_url = 'http://www.fd80.com/bookread/132711644/' + html_code + '.html'
        
        chapter_html = requests.get(chapter_url)
        chapter_text = chapter_html.text
        chapter_parser = None
        chapter_parser = BeautifulSoup(chapter_text, 'html.parser')
        
        chapter_name = li_tag.a.get_text(strip=True)
        novel_content += chapter_name + '\n'
        # 提取小说章节和正文内容
        chapter_div = chapter_parser.find_all('div', class_='novelcontent')
        if len(chapter_div) > 0:
            for p_tag in chapter_parser.find_all('div', class_='novelcontent')[0].find_all('p'):
                content = p_tag.get_text(strip=True)
                if content == '没有了' or content == '下一章' or content == '返回目录' or content == '返回封面' or content == '上一章':
                    continue
                novel_content += '    '
                novel_content += content + '\n\n'
            j += 1
            time.sleep(1)
            print('第：', j, '章已下载')

# 保存整本小说到txt文件
with open('xxx.txt', 'w', encoding='utf-8') as file:
    file.write(novel_content)
