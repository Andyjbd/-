import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

def get_data():
    # 抓取 ThisIsWhyImBroke 热门页面
    url = "https://www.thisiswhyimbroke.com/trending/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    items = soup.select('.item-list')[:30] # 抓取前30个
    html_content = "<h2>今日热门产品清单</h2><ul>"
    
    for item in items:
        try:
            title = item.select_one('h2 a').text
            link = item.select_one('h2 a')['href']
            price = item.select_one('.price').text
            html_content += f"<li><a href='{link}'>{title}</a> - <b>{price}</b></li>"
        except:
            continue
    return html_content + "</ul>"

def send_mail(content):
    sender = os.environ['EMAIL_USER']
    password = os.environ['EMAIL_PASS']
    receiver = "ayu_best@qq.com" # <--- 这里改成你自己接收邮件的邮箱

    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = "ThisIsWhyImBroke 每日趋势报告"
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP_SSL("smtp.163.com", 465) as server: # 如果用QQ邮箱改为 smtp.qq.com
        server.login(sender, password)
        server.sendmail(sender, [receiver], msg.as_string())

if __name__ == "__main__":
    data = get_data()
    send_mail(data)
