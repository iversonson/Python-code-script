import requests
import pyquery
import bs4
import csv
import openpyxl


for k in range(20):
    url = "https://gz.lianjia.com/ershoufang/pg"+str(k)+"rs%E8%B6%8A%E7%A7%80/"
    # https://gz.lianjia.com/ershoufang/pg+3+rs+%E8%B6%8A%E7%A7%80/

    payload={  'type': ' 1',
          'query': 'https://gz.lianjia.com/ershoufang/yuexiu/?sug=%E8%B6%8A%E7%A7%80',
          'Cookie': 'lianjia_uuid=67b662d6-c131-4b55-b76a-529f22fd6ca8; select_city=440100; lianjia_ssid=c04d2d4f-20bb-4b03-94d7-f67b0923ead0'}
    headers = {'Referer': 'https://gz.lianjia.com/ershoufang/yuexiu/?sug=%E8%B6%8A%E7%A7%80',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

    response = requests.request("GET", url, headers=headers, data=payload)
    content = response.text
    soup = bs4.BeautifulSoup(content,'lxml')
    titles = soup.select('.info.clear .title')
    position = soup.select('.positionInfo')
    total_price = soup.select('.totalPrice')
    uniprice = soup.select('.unitPrice')
    house_info = soup.select('.houseInfo')
    item_num = len(titles)
    wb = openpyxl.Workbook()
    sheet = wb.active
    for i in range(item_num):
        sheet['A' + str(i+1)].value = titles[i].getText()
        sheet['B' + str(i+1)].value = position[i].getText()
        sheet['C' + str(i+1)].value = total_price[i].getText()
        sheet['D' + str(i+1)].value = house_info[i].getText()
        sheet['E' + str(i+1)].value = uniprice[i].getText()
wb.save('D:\\test\\html\\houseprice_yuexiu.xlsx')
