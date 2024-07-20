#链家
from xml import etree
import requests
from lxml import etree
import pymysql

db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='pydb',
                     charset='utf8'
                     )

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

def get_House(page):
    base_url = 'https://tj.lianjia.com/zufang/pg'
    new_url_Name = base_url + str(page)
    headers = {
        'Cookie':
            'lianjia_uuid=3836b33d-eb97-40a2-9303-6f6051c5e425; _smt_uid=6562fa51.59fd13b1; _ga=GA1.2.1608667713.1700985427; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1700985439; _jzqy=1.1700985425.1700998258.1.jzqsr=baidu.-; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218c0aa1ce47e74-0d5f8f7f06b992-26031051-850468-18c0aa1ce48e3a%22%2C%22%24device_id%22%3A%2218c0aa1ce47e74-0d5f8f7f06b992-26031051-850468-18c0aa1ce48e3a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _jzqa=1.1154932927448069400.1700985425.1701004702.1701012157.5; _jzqx=1.1700987472.1701012157.2.jzqsr=tj%2Elianjia%2Ecom|jzqct=/.jzqsr=tj%2Elianjia%2Ecom|jzqct=/ershoufang/; _qzja=1.1048687766.1700985425440.1701004701521.1701012156785.1701012489219.1701012988810.0.0.0.30.5; _ga_B3G62E46BE=GS1.2.1701012159.5.1.1701012990.0.0.0; _ga_049GGDBYWQ=GS1.2.1701012159.5.1.1701012990.0.0.0; select_city=120000; lianjia_ssid=61f28984-7896-4d70-8754-6cb54fbb3b98; GUARANTEE_POPUP_SHOW=true; GUARANTEE_BANNER_SHOW=true; login_ucid=2000000385061636; lianjia_token=2.001515496c4683b78404b8605d106ef773; lianjia_token_secure=2.001515496c4683b78404b8605d106ef773; security_ticket=tfGl5EBCovI2Jx/hKd6f4mM103Vs8Udwn59nsZ3kE56hDuUrprh40yM/KyxGNprfa1GEVlzAXTzcLwPyIKyroTR3arDkMKo/1422MipBC7CQRa96IGno9ME1E8ZfXDcHOU0h9akT7asdqMqL44Fv59mfIxs8/I3CIIBU0MQWm1U=; ftkrc_=fc8488a9-8821-491b-9586-96ffebc0d53e; lfrc_=0947d1d6-dcea-4fc5-9ab3-0a15475507c0; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYzhkMTI3OTQzYTI2NWJhYzlhMmNiYmE1ZDUzYmQ4ZGFjMjVhNjM0NTYzZTNkYmMyNjEyMDk1MzFjNjc5YzYxMGNkYTdlZWM3NGU2ZTE2NDZhM2FhMDlkYTI5ZDFjOGM5MjhmZWRjNjM1YTY1MGM5ZjlhNTAxMjNlYjI4YWJjYzE2OThjNjA0MjNjYjg0YjkyMWJkOTIyMmY2ODgxYjU3MDA2NTA1NGU4YzZhYjFjNzRmZmFlYjE4NmQ1MjhlYjBkMmY0MjM4YTUzZDc4NzI0ZWE1NDQ3ZjNiNDIzZjE0NWYyNTk0MTEzYmRkOGQwMDk0ZGM2ODEwNWEzNDBmZDIyYVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI2ZjE3ZjY2YVwifSIsInIiOiJodHRwczovL3RqLmxpYW5qaWEuY29tL3p1ZmFuZy8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==',
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    page_text_01 = requests.get(url=new_url_Name, headers=headers).text
    tree01 = etree.HTML(page_text_01)
    #房屋简介
    house_Introduce_01 = tree01.xpath('//a[@class="twoline"]/text()')
    # 房源所在区
    house_Region_01 = tree01.xpath('//p[@class="content__list--item--des"]/a[1]/text()')
    # 房源所在详细地址
    house_Address_02 = tree01.xpath('//p[@class="content__list--item--des"]/a[2]/text()')
    house_Address_03 = tree01.xpath('//p[@class="content__list--item--des"]/a[3]/text()')

    #跳转到详细页面
    new_url_Detail_01 = tree01.xpath('//a[@class="twoline"]/@href')
    i1 = 0
    for _ in range(len(house_Introduce_01)):
        new_url_Detail = 'https://tj.lianjia.com' + new_url_Detail_01[i1]
        page_text_02 = requests.get(url=new_url_Detail, headers=headers).text
        tree02 = etree.HTML(page_text_02)
        # 房源类型
        house_Type_01 = tree02.xpath('//*[@id="aside"]/ul[1]/li[2]/text()')
        house_Type = house_Type_01[0]
        #房源面积
        house_Area_01 = tree02.xpath('//*[@id="info"]/ul[1]/li[2]/text()')
        house_Area = house_Area_01[0]
        # 房源楼层
        house_floor_01 = tree02.xpath('//*[@id="info"]/ul[1]/li[8]/text()')
        house_floor = house_floor_01[0]
        # 房源朝向
        house_Direction_01 = tree02.xpath('//*[@id="info"]/ul[1]/li[3]/text()')
        house_Direction = house_Direction_01[0]
        # 房源租赁价格
        house_Price_01 = tree02.xpath('//*[@id="aside"]/div[1]/span/text()')
        house_Price = house_Price_01[0]
        #房屋采暖
        house_Heating_01 = tree02.xpath('//*[@id="info"]/ul[1]/li[17]/text()')
        house_Heating = house_Heating_01[0]
        #租赁方式
        house_Lease_01 = tree02.xpath('//*[@id="aside"]/ul[1]/li[1]/text()')
        house_Lease = house_Lease_01[0]

        print( house_Introduce_01[i1] + '//' + house_Type + '//' + house_Area + '//' + house_floor + '//' + house_Direction + '//' + house_Price + '//' + house_Heating + '//' + house_Lease)

        house_Address_01 = house_Region_01[i1] + '-' + house_Address_02[i1] + '-' + house_Address_03[i1]
        house_Region = house_Region_01[i1]
        house_Introduce = house_Introduce_01[i1]
        sql = "INSERT INTO house (house_Introduce, house_Region, house_Address, house_Type, house_Area, house_floor, house_Direction, house_Price, house_Heating, house_Lease) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        par = (house_Introduce, house_Region,house_Address_01, house_Type,house_Area, house_floor, house_Direction, house_Price, house_Heating,house_Lease)
        try:
            cursor.execute(sql, par)  # 运行sql语句
            db.commit()  # 提交
            print("数据库插入成功!")
        except:
            print("数据库插入失败")
        i1 = i1 + 1.

if __name__ == '__main__':
    start_page = int(input('请输入起始的页码：'))
    end_page = int(input('请输入结束的页码：'))
    for page in range(start_page, end_page + 1):
        get_House(page)