import requests
import json
import os
import re
import time

#解析原始网页，解析json
def get_page(start_url,headers):
    try:
        r = requests.get(start_url,headers=headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        html = r.text
        ajax = json.loads(html)
        return ajax
    except:
        return  '爬取失败'

#提取图片页面链接（url)
def get_url(ajaxs):
    for ajax in ajaxs:
        url = 'http://www.nationalgeographic.com.cn'+ajax['url']
        return url

#解析图片页面
def detail_page(url,headers):
    try:
        r = requests.get(url,headers=headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return '爬取失败'

#解析详细图片链接url
def get_pics(html):
    pattern = re.compile('<a href="javascript:;" hidefocus="true"><img src="(.*?)".*?</a></div></li>',re.S)
    pic_url = re.findall(pattern,html)
    return pic_url

#保存图片至本地磁盘
def save_picture(urls):
    for url in urls:
        root = "E://国家地理每日一图//"
        path = root + url.split('/')[-1]
        try:
            if not os.path.exists(root): #不存在则执行下个语句
                os.mkdir(root)           #创建目录
            if not os.path.exists(path):
                r = requests.get(url)
                with open(path,'wb') as f:
                    f.write(r.content)
                    f.close()
                    print('图片保存成功')
            else:
                print('图片已保存')
        except:
            print('爬取错误')

def main():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                             '(KHTML, like Gecko) Chrome/62.0.3192.0 Safari/537.36'}
    i = 0
    while True:
        i += 1
        start_url = 'http://www.nationalgeographic.com.cn/index.php?m=content&c=index&a=loadmorebya&num={}&catid=39&modelid=3&parentid=11'.format(i)
        ajaxs = get_page(start_url,headers)
        if ajaxs==[]:
            break
        else:
            url = get_url(ajaxs)
            html = detail_page(url,headers)
            urls = get_pics(html)
            time.sleep(2)
            save_picture(urls)

if __name__=='__main__':
    main()