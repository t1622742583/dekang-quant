# import akshare as ak

# tool_trade_date_hist_sina_df = ak.tool_trade_date_hist_sina()
# print(tool_trade_date_hist_sina_df)

# import akshare as ak

# crypto_js_spot_df = ak.crypto_js_spot()
# print(crypto_js_spot_df)
# # 只有btc 和 LTC
# # 1.查看所有币种获取
# # 2.如果仅通过代码可获取那么
# import akshare as ak

# crypto_hist_df = ak.crypto_hist(symbol="ETH", period="每日", start_date="20151020", end_date="20201023")
# print(crypto_hist_df)
import akshare as ak
import pandas as pd

import time
from tqdm import tqdm
from data_helper.common import ALL_STOCKS_PATH, BREAD_PATH, CB_DAY_PATH, ETF_DAY_PATH, STOCK_DAY_PATH
from data_helper.geter import get_all_cb, get_day
from data_helper.saver import save_stock_day
from utils import change_code
import tushare as ts
import pandas as pd
import tushare as ts
import pandas as pd
import time
from datetime import datetime, timedelta
# pd.set_option()就是pycharm输出控制显示的设置
pd.set_option('expand_frame_repr', False)  # True就是可以换行显示。设置成False的时候不允许换行
pd.set_option('display.max_columns', None)  # 显示所有列
# pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('colheader_justify', 'centre')  # 显示居中
ts.set_token('854634d420c0b6aea2907030279da881519909692cf56e6f35c4718c')
import akshare as ak
# #  初始化pro接口
pro = ts.pro_api()
#获取可转债基础信息列表
# df = pro.cb_basic(fields="ts_code,bond_short_name,stk_code,stk_short_name,list_date,delist_date")
# codes = get_all_cb()
# print(df)


        
# codes = get_all_cb()
# df = get_day('000005.SZ',"stock",all=True)
# breed = "stock"
# store = pd.HDFStore(BREAD_PATH[breed], mode='r')

# df = store.select("000011.SZ")
# pass

# 获取期货合约列表
# futures = pro.fut_basic(exchange='DCE,CZCE,SHFE,CFFEX', fields='ts_code,symbol,name')

# 获取从2015年至今的交易日历
cal = pro.trade_cal(exchange='DCE', start_date='20150101', end_date='20230831')

# 筛选出交易日历中的交易日
trade_days = cal[cal['is_open'] == 1]['cal_date']
# 倒叙排列
trade_days = trade_days.iloc[::-1]
# 所有交易月
trade_months = trade_days.str[:6].unique()
# 初始化结果字典
result = {'日期': [], '涨的次数': [], '跌的次数': []}
df = None
# 遍历每个月
import time

for i,month in enumerate(trade_months):
    # 获取当月第一个交易日的日期
    first_day = month + '01'
    
    # 获取当月最后一个交易日的日期
    last_day = month + trade_days[trade_days > month][0][6:]
    
    # 获取当月的期货涨幅排行前5 月末收盘-月初开盘/月初开盘 排名前5
    # 月数据
    
    if df is None:
        df = ak.get_futures_daily(start_date=first_day, end_date=last_day, market="DCE")
    # 删除所有开盘价为0的数据
    df = df[df['close'] != 0]
    # 缓存
    df.to_csv("DCE.csv")
    # 基于symbol分组
    grouped = df.groupby('symbol')
    # 计算涨跌幅
    rise = (grouped['close'].last() - grouped['close'].first()) / grouped['close'].first()
    top5 = rise.sort_values(ascending=False).head(5)
    
    # 统计涨跌情况
    rise_count = 0
    fall_count = 0
    next_month = trade_months[i + 1]
    next_month_days = trade_days[trade_days.str.startswith(next_month)].to_list()
    next_month_first_day = next_month_days[0]
    next_month_last_day = next_month_days[-1]
    # next_month_first_day = "20150201"
    # next_month_last_day = "20150228"
    df = ak.get_futures_daily(start_date=next_month_first_day, end_date=next_month_last_day, market="DCE")
    # 遍历前5期货
    for symbol,row in top5.items():
        symbol_df = df[df['symbol']==symbol]
        # 删除所有开盘价为0的数据
        symbol_df = symbol_df[symbol_df['close'] != 0]
        rise = (symbol_df['close'].to_list()[-1] - symbol_df['close'].to_list()[0]) / symbol_df['close'].to_list()[0]

        if rise > 0:
            rise_count += 1
        else:
            fall_count += 1
    
    
    # 将结果添加到字典中
    result['日期'].append(month)
    result['涨的次数'].append(rise_count)
    result['跌的次数'].append(fall_count)

# 将结果转换为DataFrame并打印
df = pd.DataFrame(result)
print(df)
