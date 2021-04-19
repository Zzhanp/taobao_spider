#-*- codeing= utf-8 -*-
#@Time : 2021/1/25 19:13
import tkinter as tk
import tkinter.messagebox
from selenium import webdriver
import datetime
import time
import os
import requests
import csv
from PIL import Image, ImageTk
import jieba
import operator
import pandas as pd
from wordcloud import WordCloud
from matplotlib import pyplot as plt

# google浏览器的绝对路径
datas = []
window = tk.Tk()
window.title('淘宝爬虫')
window.geometry('400x400')
# 隐藏浏览器
# chrome_opts = webdriver.ChromeOptions()
# chrome_opts.add_experimental_option(
    # 'excludeSwitches', ['enable-automation'])
# chrome_opts.add_argument('--headless')
# chrome_opts.add_argument('--no-sandbox')
# chrome_opts.add_argument('--disable-dev-shm-usage')
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
driver = webdriver.Chrome(chrome_path)
# driver = webdriver.Chrome(chrome_path, chrome_options=chrome_opts)


def login():
    driver.get("https://www.taobao.com")
    # 获取到搜索按钮后，点击
    driver.find_element_by_xpath(
        '//*[@id="J_TSearchForm"]/div[1]/button').click()
    # 改变窗口宽度,不要最大化，会被反爬虫检测到
    driver.set_window_size(1300, 800)
    # 点击二维码扫描
    driver.find_element_by_xpath('//*[@id="login"]/div[1]/i').click()
    time.sleep(3)
    
    # 等待扫描二维码，时间短了就改一改
    while True:
        try:
            driver.find_element_by_xpath('//*[@id="login"]/div[1]/i') # 二维码是否存在
            flag = 1
        except:
            flag = 0
        # 二维码存在,判定为扫码未完成，继续等待扫码
        if flag:
            continue
        else:
            break
        time.sleep(1)  # 每隔1s检测一次是否扫描二维码
    now = datetime.datetime.now()
    print('login success:', now.strftime('%Y-%m-%d %H:%M:%S'))


def drop_scroll():
    for x in range(1, 11, 2):
        # 停一下，慢慢拉，拉快了会出问题哦
        time.sleep(0.5)
        # 代表滑动条位置
        j = x/10
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        # 运行上面的js代码
        driver.execute_script(js)

#def buy(url1):
    #driver.get(str(url1))


def get_gooods(serach1):
    # 获取分页面总数，由于自己的需求，没有翻页，翻页需要的最大值
    # 这里提醒大家，如果自己要翻页，请不要点击下一页按钮，也会被检测出来，（可观察后，改变地址栏）
    # token = driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[1]').text
    # print(token)
    # 序号
    xh = 0
    # 分析淘宝页面后，获取商品div里面的数据
    divs = driver.find_elements_by_xpath(
        '//div[@class="items"]/div[@class="item J_MouserOnverReq  "]')
    # 遍历每个divs，获取商品详细信息
    for div in divs:
        # print(search1)
        xh += 1
        # 获取图片地址
        img = div.find_element_by_xpath(
            './/div[@class="pic"]/a/img').get_attribute('data-src')
        # 拼接全地址，用于下载
        src_path = "https:"+img
        # 请求图片地址，并进行下载，重命名，格式为：分类_序号，没有img文件夹请自己新建
        a = os.getcwd()
        try:
            os.mkdir(a+'\\{}_img'.format(s.get()))
        except:
            p = 1
        open("./{}_img/{}_{}.jpg".format(s.get(), serach1, xh), mode="wb").write(requests.get(src_path).content)
        # 获取标题
        title = div.find_element_by_css_selector('div.row.row-2.title').text
        # 获取价格
        price = div.find_element_by_xpath(
            './/div[@class="price g_price g_price-highlight"]/strong').text+'元'
        # 付款人数（销售数）
        num = div.find_element_by_xpath('.//div[@class="deal-cnt"]').text
        # 商品链接
        url = div.find_element_by_xpath('.//div[@class="row row-2 title"]/a').get_attribute('href')
        # 一条数据
        product = {'分类': serach1, '序号': xh, '标题': title,
                   'imgurl': img, '价格': float(price.strip("元")), '销售数': num, '链接': str(url)}
        print(product)
        # 向数组添加一条数据
        datas.append(product)


def searchs(serach1):
        '''print(serach1)
        # 获取文本框
        print(driver.current_url)
        driver.get_screenshot_as_file("erweima.png")'''
        datas = []
        serachinput = driver.find_element_by_xpath('//*[@id="q"]')
        # 清空文本框
        serachinput.clear()
        # 输入查询内容
        serachinput.send_keys(serach1)
        # 点击搜索按钮
        driver.find_element_by_xpath('//*[@id="J_SearchForm"]/button').click()
        # 拉动侧边滑动条，使页面数据加载完全
        drop_scroll()
        # 获取商品信息
        get_gooods(serach1)


def save(data):
    # csv文件表头
    header = ['分类', '序号', '标题', 'imgurl', '价格', '销售数', '链接']
    with open('{}.csv'.format(s.get()), 'a', newline='') as f:
        # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        writer = csv.DictWriter(f, fieldnames=header)
        # 写入列名（表头）
        writer.writeheader()
        # 写入数据
        writer.writerows(data)
    s4.set('总共{}件商品,请输入您要搜索的序号'.format(len(data)))


def get_data(data):

    searchs(data)
    save(datas)


def shows(num1, serch1):
    sh = tk.Toplevel(window)
    sh.title('商品信息')
    sh.geometry('1500x1000')
    img1 = Image.open("./{}_img/{}_{}.jpg".format(serch1, serch1, num1))
    global img_png
    img_png = ImageTk.PhotoImage(img1)
    label_img = tk.Label(sh, image=img_png)
    label_img.place(x=100, y=100)
    #b2 = tk.Button(sh, text='跳转', width=10, height=1, command=lambda: buy(datas[int(num1)-1].get('商品链接')))
    #b2.place(x=1200, y=100)
    t1 = tk.Label(sh, text='商品：{}'.format(str(datas[int(num1)-1].get('标题'))), bg='white', font=('Arial', 10),
                  width=60, height=1)
    t1.place(x=1000, y=200)
    t2 = tk.Label(sh, text="价格：{}".format(str(datas[int(num1)-1].get('价格'))), bg='white', font=('Arial', 12),
                  width=20, height=1)
    t2.place(x=1200, y=400)
    t3 = tk.Label(sh, text="销售数：{}".format(str(datas[int(num1)-1].get('销售数'))), bg='white', font=('Arial', 12),
                  width=20, height=1)
    t3.place(x=1200, y=600)


s = tk.StringVar()
s.set('请输入搜索关键词')
e1 = tk.Entry(show=None, textvariable=s, font=('Arial', 25), width=22)   # 搜索框
e1.place(x=0, y=0)
n = tk.StringVar()
e2 = tk.Entry(show=None, textvariable=n, font=('Arial', 10), width=10)   # 搜索框
e2.place(x=300, y=200)
login()
s4 = tk.StringVar()
t4 = tk.Label(textvariable=s4, bg='white', font=('Arial', 12),
              width=30, height=1)
t4.place(x=0, y=200)
b1 = tk.Button(text='搜索', width=10, height=1, command=lambda: get_data(s.get()))
b1.place(x=100, y=60)
b3 = tk.Button(text='显示', width=10, height=1, command=lambda: shows(n.get(), s.get()))
b3.place(x=100, y=300)
b4 = tk.Button(text='退出', width=10, height=1, command=lambda: window.quit())
b4.place(x=200, y=300)
window.mainloop()


#中文显示
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

#读取数据
key = s.get()
data = pd.read_csv('{}.csv'.format(s.get()),encoding='gb18030',engine='python')
#分析价格分布
plt.figure(figsize=(16,9))
plt.hist(data['价格'],bins=20,alpha=0.6)
plt.title('价格频率分布直方图')
plt.xlabel('价格')
plt.ylabel('频数')
plt.savefig('{}价格分析.png'.format(s.get()))


# 制作词云
content = ''
for i in range(len(data)):
    content += data['标题'][i]
wl = jieba.cut(content,cut_all=True)
wl_space_split = ' '.join(wl)
wc = WordCloud('simhei.ttf',
               background_color='white', # 背景颜色
               width=1000,
               height=600,).generate(wl_space_split)
wc.to_file('{}.png'.format(s.get()))