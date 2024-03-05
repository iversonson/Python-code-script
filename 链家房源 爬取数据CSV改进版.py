import requests
import bs4
import csv

# 打开CSV文件，以UTF-8编码和换行符写入
with open('houseprice_yuexiu_dongshankou.csv', 'w', encoding='utf-8', newline='') as file:
    file.write('\ufeff')
    writer = csv.writer(file)

    # 写入表头
    header = ["标题", "位置", "总价", "房屋信息", "单价"]
    writer.writerow(header)

    # 遍历页面
    for k in range(100):
        url = f"https://gz.lianjia.com/ershoufang/pg{k}rs越秀东山口/"

        payload = {
            'type': '1',
            'query': 'https://gz.lianjia.com/ershoufang/yuexiu/?sug=越秀',
            'Cookie': 'lianjia_uuid=67b662d6-c131-4b55-b76a-529f22fd6ca8; select_city=440100; lianjia_ssid=c04d2d4f-20bb-4b03-94d7-f67b0923ead0'
        }
        headers = {
            'Referer': requests.utils.quote('https://gz.lianjia.com/ershoufang/yuexiu/?sug=越秀'),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        content = response.text
        soup = bs4.BeautifulSoup(content, 'lxml')

        titles = soup.select('.info.clear .title')
        position = soup.select('.positionInfo')
        total_price = soup.select('.totalPrice')
        uniprice = soup.select('.unitPrice')
        house_info = soup.select('.houseInfo')

        item_num = len(titles)
        for i in range(item_num):
            content_list = [titles[i].getText(), position[i].getText(), total_price[i].getText(),
                            house_info[i].getText(), uniprice[i].getText()]
            writer.writerow(content_list)


