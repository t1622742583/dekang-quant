import datetime
import os
import random
import re
import requests
import pandas as pd
from tqdm import tqdm
import time
ALL_STOCKS_PATH = "data/all_stocks.csv"
SAVE_DIR = "data/comment"
from data_helper.geter import get_all_stocks
def get_all_stocks():
    pd.read_csv(ALL_STOCKS_PATH)["ts_code"].values.tolist()

delete_refix = re.compile('<hx_stock>.+</hx_stock>')
delete_img_refix = re.compile('<img.+/>')


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36 Edg/107.0.1418.42',
    'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}

def add_stock_postfix(code):
    if code.isdigit():
        prefix = code[:2]
    if prefix in ['60', '90']:
        return code + '.SH'
    elif prefix in ['00', '30']:
        return code + '.SZ'
    return code + '.BJ'  # 默认为北京证券交易所
def get_proxies():
    url = "http://api.proxy.ipidea.io/getProxyIp?num=10&return_type=json&lb=1&sb=0&flow=1&regions=&protocol=http"
    response = requests.get(url)
    res = response.json()
    if res["code"] == 0:
        return res["data"]

def get_comments(stock_code,bar=None,proxies=None):
# store_all = pd.HDFStore('data/comment.h5')
# breed = "comment"
    save_stock_code = add_stock_postfix(stock_code)
    save_path = os.path.join(SAVE_DIR,f"{save_stock_code}.parquet")
    if os.path.exists(save_path):
        return
    with requests.Session() as session:
        page = 1
        if proxies:
            proxie = random.choice(proxies)
            session.proxies = {'http': f'http://{proxie["ip"]}:{proxie["port"]}'}
        response = session.get('https://t.10jqka.com.cn/lgt/cache/indexCache', params={'stockcode': stock_code},
                                    headers=headers, timeout=10)
        res = response.json()
        if res["status_code"] == 0:
            market_id = res["result"]["initData"]["marketId"]
            market_id = str(market_id)
        else:
            print(f"获取{stock_code}失败")
            return
        un_out = True
        all_comments = []
        while un_out:
            bar.set_description(f"{stock_code}第{page}页评论")
            # print(f"正在获取{stock_code}第{page}页评论")
            # if page > 10:
            #     break
            params = {
                'page': str(page),
                'page_size': '15',
                'sort': 'publish',
                'code': stock_code,
                'market_id': market_id,
            }
            if proxies:
                proxie = random.choice(proxies)
                session.proxies = {'http': f'http://{proxie["ip"]}:{proxie["port"]}'}
            response = session.get('https://t.10jqka.com.cn/lgt/post/open/api/forum/post/recent', params=params,
                                        headers=headers)
            res = response.json()
            if res['status_code'] != 0:
                break
            comments = res["data"]["feed"]
            if comments:
                for comment in comments:
                    _time = datetime.datetime.fromtimestamp(comment["ctime"])
                    create_time = _time.strftime("%H:%M:%S")
                    create_date = _time.date().strftime("%Y-%m-%d")
                    comment = delete_refix.sub('', comment["content"]).strip()
                    comment = delete_img_refix.sub('', comment).strip()

                    # df = pd.DataFrame([{"code": save_stock_code, "date": create_date,"create_time":create_time, "comment": comment}])
                    # store_all.append(breed, df, data_columns=True, index=False)
                    #
                    all_comments.append(
                        [
                            create_date,
                            create_time,
                            comment
                        ]
                    )
            else:
                un_out = False
                break
            # 随机sleep 0.1-0.5秒
            time.sleep(random.randint(1, 5) / 10)
            page += 1
    
    all_comments_df = pd.DataFrame(all_comments, columns=["date", "create_time", "comment"])
    # 写入到parquet
    all_comments_df.to_parquet(save_path, index=False)
    # 随机sleep 1-3秒
    time.sleep(random.randint(1, 3))
# store_all.close()

def main():
    stocks = get_all_stocks(bj=True,load_cache=True)
    bar = tqdm(stocks)
    for stock in bar:
        # 去除后缀
        stock = stock.split('.')[0]
        # bar.set_description(stock)
        proxies = get_proxies()
        get_comments(stock,bar,proxies)
        
        




if __name__ == '__main__':
    main()
