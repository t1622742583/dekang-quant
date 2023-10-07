import os
import sys
# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取三级父目录的绝对路径
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)
import pandas as pd
from tqdm import tqdm
import tushare as ts
import akshare as ak
import pandas as pd

from data_helper.common import ALL_CB_PATH, ALL_ETF_PATH, ALL_STOCKS_PATH, ALL_TRADE_DATE_PATH, BREAD_PATH, CACHE_DAY_PATH, ETF_DAY_PATH
from data_helper.saver import save_etf_day
from utils import change_code
ts.set_token('854634d420c0b6aea2907030279da881519909692cf56e6f35c4718c')

#  初始化pro接口
pro = ts.pro_api()
def get_all_etf():
    etf_df = ak.fund_etf_category_sina("ETF基金")
    # 保留'代码'列和'名称'列
    etf_df = etf_df.iloc[:, [0, 1]]
    # 保存为csv文件(覆盖)
    etf_df.to_csv(ALL_ETF_PATH, index=False)
    return etf_df['代码'].tolist()
# def get_all_cb(reture_stock=False,load_cache=False):
#     if load_cache:
#         # return [(cb,stock),]
#         return pd.read_csv(ALL_CB_PATH)[["代码", "正股代码"]].values.tolist()
#     def determine_market(code):
#         if code.startswith("6"):
#             return "sh"  # 沪市前缀
#         else:
#             return "sz"  # 深市前缀
#     # https://app.jisilu.cn/data/cbnew/#cb 获取
#     cookie = "kbz__Session=b0gt86t1f0o4hu8ncm21iaa1a5; Hm_lvt_164fe01b1433a19b507595a43bf58262=1692500155; kbz_newcookie=1; kbz__user_login=1ubd08_P1ebax9aXwZWukamwlaOXpZqwlunN6tXt0OXcv82M17HYnKmh2JLYxqrckajGpa-rod-hqMTakaOwl6CV2bKWpKbh4MbUvp6pmqmZqammirSZuLbUvp6pl6mTqamlmq6lmJ2jtrTWvpuu4_Pe1eXNppekkZOguNnP2Ojs3Jm6y4KnkaGonJC43eernbSM75iqipO50eDN2dDay8TV65GrlKqmlKaBnMS9vca4o4Liyt7dgbfG1-Tkkpmv39TlztinkqGWoqmjmaecl7XXx9Tqyp-Wp7CjnK-MvMbdkKSplp6RoqqumaqaqZKp; Hm_lpvt_164fe01b1433a19b507595a43bf58262=1692500163; SERVERID=5452564f5a1004697d0be99a0a2e3803|1692500168|1692500151"
#     cb_df = ak.bond_cb_jsl(cookie=cookie)
#     cb_df["市场"] = cb_df["正股代码"].apply(determine_market)
#     cb_df["代码"] = cb_df["市场"] + cb_df["代码"]
#     cb_df.to_csv(ALL_CB_PATH)
#     if reture_stock:
#         # return [(cb,stock),]
#         return cb_df[["代码", "正股代码"]].values.tolist()
#     else:
#         # return [cb,]
#         return cb_df["代码"].tolist()
def get_all_cb(reture_stock=True,use_cache=False):
    if use_cache:
        return pd.read_csv(ALL_CB_PATH)[["ts_code", "stk_code"]].values.tolist()
    cb_df = pro.cb_basic()
    cb_df.to_csv(ALL_CB_PATH)
    if reture_stock:
        # return [(cb,stock),]
        return cb_df[["ts_code", "stk_code"]].values.tolist()
    else:
        # return [cb,]
        return cb_df["ts_code"].tolist()
def get_all_stocks(bj=False,load_cache=False):
    if load_cache:
        return pd.read_csv(ALL_STOCKS_PATH)["ts_code"].values.tolist()
    df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    # 去除 ts_code 中包含.BJ的所有行
    if not bj:
        df = df[~df['ts_code'].str.contains('.BJ')]
    df["code"] = df["ts_code"].apply(lambda x: change_code(x))
    df.sort_values(by='list_date', inplace=True)
    df.to_csv(ALL_STOCKS_PATH, index=False)
    return df["ts_code"].values.tolist()
def get_day(code,breed="etf",start_date=None, end_date=None,all=False):
    """获取日线数据"""
    if all:
        where = None
    else:
        where = f"date>='{start_date}' and date<='{end_date}'"
    with pd.HDFStore(BREAD_PATH[breed]) as store:
        df = store.select(code, where=where)
    # date作为index
    # df.set_index('date',inplace=True)
    return df
def get_custom_day(data_path:str=None):
    """获取自定义数据"""
    if data_path.endswith(".csv"):
        df = pd.read_csv(data_path)
    elif data_path.endswith(".h5"):
        df = pd.read_hdf(data_path, key="all")
    # df['date'] = pd.to_datetime(df['date'])
    # df.set_index('date', inplace=True)
    # 获取索引名称
    index_name = df.index.name
    # 恢复索引但不删除索引列
    df.reset_index(inplace=True)
    # 重命名索引
    # df.rename(columns={index_name: 'date'}, inplace=True)
    codes = df['code'].unique().tolist()
    return codes,df
def get_all_day(breed="cb",start_date="2015-01-01", end_date=pd.Timestamp.today().strftime('%Y-%m-%d'),cache=False,use_cache=False):
    """获取日线数据"""
    if use_cache:
        with pd.HDFStore(CACHE_DAY_PATH) as store:
            df = store.select(breed)
        # 去重
        df.drop_duplicates(subset=['date', 'code'], keep='first', inplace=True)
        # 保存为HDF5文件

        # df.to_hdf(CACHE_DAY_PATH, key=breed, mode='w')
        
        codes = df['code'].unique().tolist()
        return codes,df
    # 打开HDF5文件
    store = pd.HDFStore(BREAD_PATH[breed], mode='r') # mode='r' 只读模式
    # 用于存储股票历史数据的列表
    stock_data_list = []
    # 遍历HDF5文件中的所有键（股票代码）
    # 所有标的
    store_keys = store.keys()
    # 进度条
    progress_bar = tqdm(store_keys, desc="load", unit=f" {breed}")
    for code in store_keys:
        progress_bar.set_postfix(code=code)
        # 使用select函数查询满足日期条件的数据
        query = f"`date` >= '{start_date}' & `date` <= '{end_date}'"
        stock_data = store.select(code, where=query)
        # 加入code列
        stock_data['code'] = code.split('/')[-1]
        # 添加到股票数据列表
        stock_data_list.append(stock_data)

    # 关闭HDF5文件
    store.close()

    # 将所有股票数据纵向合并
    merged_data = pd.concat(stock_data_list, ignore_index=True)

    
    if cache:
        with pd.HDFStore(CACHE_DAY_PATH) as store:
            store.put(breed, merged_data)
    return store_keys,merged_data
def get_all_day_ml(breed="cb", start_date="2015-01-01", end_date=pd.Timestamp.today().strftime('%Y-%m-%d'), cache=False, use_cache=False):
    """获取日线数据"""
    if use_cache:
        with pd.HDFStore(CACHE_DAY_PATH) as store:
            df = store.select(breed+'ml5')
        # 去重
        df.drop_duplicates(subset=['date', 'code'], keep='first', inplace=True)
        # 保存为HDF5文件

        # df.to_hdf(CACHE_DAY_PATH, key=breed, mode='w')

        codes = df['code'].unique().tolist()
        return codes, df

    # 打开HDF5文件
    store = pd.HDFStore(BREAD_PATH[breed], mode='r')  # mode='r' 只读模式
    # 用于存储股票历史数据的列表
    stock_data_list = []
    # 遍历HDF5文件中的所有键（股票代码）
    # 所有标的
    store_keys = store.keys()
    # 进度条
    # 
    # 
    progress_bar = tqdm(store_keys, desc="load", unit=f" {breed}")
    for code in progress_bar:
        progress_bar.set_postfix(code=code)
        # 使用select函数查询满足日期条件的数据
        query = f"`date` >= '{start_date}' & `date` <= '{end_date}'"
        stock_data = store.select(code, where=query)
        # 加入code列
        stock_data['code'] = code.split('/')[-1]
        
        # 创建涨跌列（up_down）
        stock_data['up_down'] = (stock_data['close'].shift(-5) > stock_data['close']).astype(int)

        # 删除最后一天
        stock_data = stock_data.iloc[:-5]

        # 添加到股票数据列表
        stock_data_list.append(stock_data)

    # 关闭HDF5文件
    store.close()

    # 将所有股票数据纵向合并
    merged_data = pd.concat(stock_data_list, ignore_index=True)

    if cache:
        with pd.HDFStore(CACHE_DAY_PATH) as store:
            store.put(breed+"ml5" , merged_data)

    return store_keys, merged_data
def get_trade_days(start_date=None, end_date=None):
    """ 获取所有交易日 """
    df = pd.read_csv(ALL_TRADE_DATE_PATH)
    if start_date is not None:
        df = df[df['trade_date'] >= start_date]
    if end_date is not None:
        df = df[df['trade_date'] <= end_date]
    return df['trade_date'].tolist()
def lack_data(breed='etf',code=None,start_date=None, end_date=None):
    """获取缺失数据"""
    if breed == 'etf':
        save_etf_day(code)

class HqMm:
    def __init__(self):
        self.store = pd.HDFStore(r'data\research\cache_all.h5')
        self.keys = self.store.keys()
    def get(self,date="2021-08-31",columns=None):
        """获取某一天的行情"""
        date = date.replace("-","")
        if '/'+date in self.keys:
            df = self.store.get(date)
            if columns:
                df = df[columns]
            # 去重
            df.drop_duplicates(subset=['code'], keep='first', inplace=True)
            # 保存
            # self.store.put(date, df, data_columns=True, index=False,format="f")
            return df
        df = self.store.select("stock", where=f"date == '{date}'")
        # 存入
        df.drop_duplicates(subset=['date', 'code'], keep='first', inplace=True)
        self.store.put(date, df, data_columns=True, index=False,format="f")
        self.keys = self.store.keys()
        if columns:
            df = df[columns]
        
        return df
    def __del__(self):
        self.store.close()

# 