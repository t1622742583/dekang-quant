import time
from typing import Any
import akshare as ak
import numpy as np
import pandas as pd
from tqdm import tqdm
from data_helper.common import BREAD_PATH, CACHE_DAY_PATH
from data_helper.geter import get_all_day
# stock_zh_a_hist_min_em_df = ak.stock_zh_a_hist_min_em(symbol="000001", start_date="2023-08-31 09:00:00", end_date="2023-08-31 09:30:00", period='1', adjust='')
# stock_zh_a_hist_pre_min_em_df = ak.stock_zh_a_hist_pre_min_em(symbol="000001",end_time="09:30:00")
# print(stock_zh_a_hist_pre_min_em_df)
# # print(stock_zh_a_hist_min_em_df) 
def delete_columns(df,target_columns):
    """删除df中的列"""
    # baohan_columns = []
    for column in target_columns:
        if column in df.columns:
            df.drop(columns=[column], inplace=True)
    # print(f"包含的列:{baohan_columns}")
# buyao_columns = ['int_income', 'comm_income', 'n_commis_income', 'n_oth_income', 'n_oth_b_income', 'oth_b_income', 'forex_gain', 'int_exp', 'comm_exp', 'oper_exp', 'other_bus_cost', 'update_flag', 'fv_value_chg_gain', 'oth_compr_income', 'ass_invest_income', 'continued_net_profit', 'dt_eps_yoy']
buyao_columns = ['report_type', 'comp_type', 'end_type', 'basic_eps', 'diluted_eps', 'total_revenue', 'revenue', 'int_income', 'comm_income', 'n_commis_income', 'n_oth_income', 'n_oth_b_income', 'oth_b_income', 'fv_value_chg_gain', 'invest_income', 'ass_invest_income', 'forex_gain', 'total_cogs', 'int_exp', 'comm_exp', 'biz_tax_surchg', 'admin_exp', 'assets_impair_loss', 'oper_exp', 'other_bus_cost', 'operate_profit', 'non_oper_income', 'non_oper_exp', 'total_profit', 'income_tax', 'n_income', 'n_income_attr_p', 'minority_gain', 'oth_compr_income', 't_compr_income', 'compr_inc_attr_p', 'compr_inc_attr_m_s', 'continued_net_profit', 'update_flag']
paichu_stocks = []
def save_to_all(breed="stock"):
    """获取日线数据"""
    global buyao_columns
    # 打开HDF5文件
    store = pd.HDFStore(BREAD_PATH[breed], mode='r') # mode='r' 只读模式
    store_all = pd.HDFStore('data/cache_all.h5')
    # 清空store_all
    try:
        store_all.remove(breed)
    except KeyError:
        pass
    # 遍历HDF5文件中的所有键（股票代码）
    store_keys = store.keys()
    # 进度条
    progress_bar = tqdm(store_keys, desc="load", unit=f" {breed}")
    for code in progress_bar:
        progress_bar.set_postfix(code=code)
        # 使用select函数查询满足日期条件的数据
        stock_data = store.get(code)
        # 加入code列
        stock_data['code'] = code.split('/')[-1]
        # 删除int_income列
        # stock_data.drop(columns=["int_income"], inplace=True)
        # 获取所有类型为object的列
        
        # delete_columns(stock_data,buyao_columns)
        stock_data.drop(columns=buyao_columns, inplace=True)
        object_columns = stock_data.select_dtypes(include=['object']).columns.to_list()
        # 删除code
        object_columns.remove("code")
        
        if object_columns:
            paichu_stocks.append(code)
            progress_bar.set_postfix(sheqi=len(paichu_stocks))
            progress_bar.set_postfix(queshi=code)
            # print(f"缺失,code:{code},object_columns:{len(object_columns)}")
            continue
            # buyao_columns += object_columns
            # print("重新运行",buyao_columns)
            
            # save_to_all()
            # store_all.close()
            # store.close()
            # return
        # if code == "/sh600004":
        #     object_columns = stock_data.select_dtypes(include=['object']).columns
        #     print(f"object_columns:{object_columns}")
        # if stock_data.empty:
        #     print(f"empty:{code}")
        #     continue
        # stock_data.drop(columns=["comm_income"], inplace=True)
        # with pd.HDFStore('data/cache_all.h5') as store_all:
        store_all.append(breed, stock_data, data_columns=True, index=False)

    # 关闭HDF5文件
    store_all.close()
    store.close()
# save_to_all()

# 1.把所有stock放到一个表格中
# 2.基于日期筛选出所有股票的同一天数据，放到另一个表格
class HqMm:
    def __init__(self):
        self.store = pd.HDFStore('data/cache_all.h5')
        self.keys = self.store.keys()
    def get(self,date="2021-08-31",columns=None):
        """获取某一天的行情"""
        date = date.replace("-","")
        if '/'+date in self.keys:
            df = self.store.get(date)
            if columns:
                df = df[columns]
            return df
        df = self.store.select("stock", where=f"date == '{date}'")
        # 存入
        self.store.put(date, df, data_columns=True, index=False,format="f")
        self.keys = self.store.keys()
        if columns:
            df = df[columns]
        return df
hm = HqMm()
start_time = time.time()
df = hm.get("2021-08-31",columns=["code","close"])
end_time = time.time()
print(f"耗时:{end_time-start_time}")
print(df)


