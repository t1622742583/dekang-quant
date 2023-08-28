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

# #  初始化pro接口
pro = ts.pro_api()
#获取可转债基础信息列表
# df = pro.cb_basic(fields="ts_code,bond_short_name,stk_code,stk_short_name,list_date,delist_date")
# codes = get_all_cb()
# print(df)


        
# codes = get_all_cb()
# df = get_day('000005.SZ',"stock",all=True)
breed = "stock"
store = pd.HDFStore(BREAD_PATH[breed], mode='r')

df = store.select("000011.SZ")
pass