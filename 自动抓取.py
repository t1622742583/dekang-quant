from datetime import datetime, timedelta
import os
import akshare as ak
import tushare as ts
import pandas as pd
from tqdm import tqdm
from data_helper.common import BREAD_PATH, CACHE_DAY_PATH, STOCK_Trade_PATH
from data_helper.geter import get_all_day
pd.set_option('expand_frame_repr', False)  # True就是可以换行显示。设置成False的时候不允许换行
pd.set_option('display.max_columns', None)  # 显示所有列
# pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('colheader_justify', 'centre')  # 显示居中
ts.set_token('854634d420c0b6aea2907030279da881519909692cf56e6f35c4718c')
# #  初始化pro接口
pro = ts.pro_api()
def save_cb_market(start_date="20150101",end_date="20230816"):
    # cd_df = pro.cb_daily(trade_date='20230904') # 拿不到当天行情
    # df = pro.daily(trade_date='20230904') # 拿不到当天行情
    # 获取所有可转债实时数据
    # 遍历所有可转债
    # stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    stock_financial_abstract_ths_df = ak.stock_financial_abstract_ths(symbol="000063", indicator="按报告期")
    # stock_financial_analysis_indicator_df= ak.stock_financial_analysis_indicator(symbol="000063")
    # 请求股票个次，纵向合并
    # v 方案一：akshare中基于几个请求接口获取，缺点：1.可转债需要cookie，（可以每日手动配置但麻烦），2.多表融合复杂度高
    # 方案一：同花顺
    pass
    # 1.获取转债日线行情 
    # fields = ['ts_code', 'trade_date', 'pre_close', 'open', 'high', 'low', 'close', 'change', 'pct_chg', 'vol', 'amount','bond_value','bond_over_rate','cb_value','cb_over_rate']
    # cb_df = pro.cb_daily(ts_code=code,start_date=start_date,end_date=end_date,fields=fields)
    # if cb_df.empty:
    #     # 未获取到数据:未上市/
    #     return
    # # 修改trade_date列名为date
    # cb_df.rename(columns={"trade_date": "date"}, inplace=True)
    # # 修改date列类型为datetime
    # cb_df['date'] = pd.to_datetime(cb_df['date'])
    # # 3.获取正股日线行情
    # stock_df = get_day(stock_code,"stock",all=True)
    # # 4.修改列名 open->open_stock,close->close_stock,high->high_stock,low->low_stock,vol->vol_stock,amount->amount_stock
    # stock_df.rename(columns={"open": "open_stock", "close": "close_stock", "high": "high_stock", "low": "low_stock", "vol": "vol_stock", "amount": "amount_stock"}, inplace=True)
    # # 5.合并转债日线行情和正股日线行情
    # merged_df = pd.merge(cb_df, stock_df, on="date", how="outer")
    # # 去除ts_code列
    # merged_df.drop(columns=["ts_code"], inplace=True)
    # # merged_df = merged_df[merged_df['close'].notna()]  # 删除停牌数据（使用层找不到数据要使用邻近算法）
    # # 基于date列排序
    # merged_df.sort_values("date", inplace=True)
    # # 6.保存到hdf文件
    # with pd.HDFStore(CB_DAY_PATH) as store:
    #     store.put(code, merged_df, data_columns=True,format="table")
def get_fin(ts_code,today):
    # 获取当日财务指标数据
    lastyear_date = datetime.strptime(today, '%Y%m%d') - timedelta(days=365)  # str转time
    fina_start_date = datetime.strftime(lastyear_date, '%Y%m%d')  # time转str
    # df_fina = pro.fina_indicator(ts_code=ts_code, start_date=fina_start_date)
    fina_columns = ['ann_date','end_date','eps', 'dt_eps', 'total_revenue_ps', 'revenue_ps', 'capital_rese_ps', 'surplus_rese_ps', 'undist_profit_ps', 'extra_item', 'profit_dedt', 'assets_turn', 'op_income', 'fcff', 'retained_earnings', 'diluted2_eps', 'bps', 'ocfps', 'retainedps', 'cfps', 'netprofit_margin', 'profit_to_gr', 'adminexp_of_gr', 'impai_ttm', 'op_of_gr', 'roe', 'roe_waa', 'roe_dt', 'npta', 'roe_yearly', 'debt_to_assets', 'assets_to_eqt', 'dp_assets_to_eqt', 'debt_to_eqt', 'eqt_to_debt', 'ocf_to_debt', 'roa_yearly', 'roa_dp', 'fixed_assets', 'profit_to_op', 'q_roe', 'q_dt_roe', 'q_npta', 'q_ocf_to_sales', 'basic_eps_yoy', 'dt_eps_yoy', 'cfps_yoy', 'op_yoy', 'ebt_yoy', 'netprofit_yoy', 'dt_netprofit_yoy', 'ocf_yoy', 'roe_yoy', 'bps_yoy', 'assets_yoy', 'eqt_yoy', 'tr_yoy', 'or_yoy', 'q_sales_yoy', 'q_op_qoq', 'equity_yoy']
    df_fina = pro.fina_indicator(ts_code=ts_code, start_date=fina_start_date,fields=','.join(fina_columns))
    
    return df_fina
def code_add_postfix(code):
    """给code加上后缀"""
    if code.startswith("6"):
        code = code + ".SH"
    elif code.startswith("0") or code.startswith("3"):
        code = code + ".SZ"
    else:
        code = code + ".BJ"
    return code
def save_stock_market():
    # 获取当前日期
    today = pd.Timestamp.today().strftime('%Y%m%d')
    # today = "20230928"
    today_datetime = datetime.strptime(today, '%Y%m%d')  # str转time
    df = ak.stock_zh_a_spot_em()
    columns = ["代码","最高","最低","今开","最新价","昨收","涨跌幅","成交量","成交额"]
    # rename
    df = df[columns]
    
    df.rename(columns={"代码": "code","最高":"high","最低":"low","今开":"open","最新价":"close","昨收":"pre_close","涨跌幅":"change","成交量":"vol","成交额":"amount"}, inplace=True)
    df['code'] = df['code'].apply(code_add_postfix)
    df["date"] = today_datetime
    # df = pro.daily(trade_date=today)
    # 修改trade_date列名为date
    # df.rename(columns={"trade_date": "date"}, inplace=True)
    # df.rename(columns={"ts_code": "code"}, inplace=True)
    # 修改date列类型为datetime
    # df['date'] = pd.to_datetime(df['date'])
    # ts_code列类型转换
    # 基于ts_code列分组
    grouped = df.groupby('code')
    # 遍历分组
    merged_dfs = []
    for code, group in grouped:
        # 获取当日财务指标数据
        df_fina = get_fin(code,today)
        df_fina["date"] = today_datetime
        # 合并
        merged_df = pd.merge(group, df_fina, how="outer",on="date")
        merged_dfs.append(merged_df)
    # 合并所有
    merged_df = pd.concat(merged_dfs)
    # 写入当天行情
    parquet_name = f"{today}.parquet"
    merged_df.to_parquet(os.path.join(STOCK_Trade_PATH,parquet_name), index=False)
    pass
    
save_stock_market()
# 1.定时任务 14:55，2.获取当日行情，3.保存到hdf文件/parquet文件
# 解决财务指标多次请求获取问题
# 1.监听式 有更新则获取，反之使用历史数据
# 2.整体式获取,减少请求次数
# 3.akshare获取
# 4.从早上开始获取