from datetime import datetime, timedelta
import akshare as ak
import pandas as pd

from data_helper.common import CB_DAY_PATH, ETF_DAY_PATH, STOCK_DAY_PATH
from data_helper.common import ALL_TRADE_DATE_PATH
import time
from tqdm import tqdm
import tushare as ts




from utils import change_code

pro = ts.pro_api('854634d420c0b6aea2907030279da881519909692cf56e6f35c4718c')

def save_etf_day(code):
    df = ak.fund_etf_hist_sina(symbol=code)
    # 时间列类型转换
    df['date'] = pd.to_datetime(df['date'])
    # df.set_index('date', inplace=True)
    with pd.HDFStore(ETF_DAY_PATH) as store:
        store.put(code, df, data_columns=True)


def save_all_etf_day():
    from data_helper.geter import get_all_etf
    codes = get_all_etf()
    progress_bar = tqdm(codes, desc="Saving ETF data", unit=" ETF")
    for code in progress_bar:
        success = False
        while not success:
            try:
                save_etf_day(code)
                success = True
            except Exception as e:
                print(f"Error occurred for ETF {code}: {e}")
                time.sleep(5)  # 延迟5秒重试
    # 保存当前昨天为最后更新日期
    # with pd.HDFStore(ETF_DAY_PATH) as store:
    #     # 昨天
    #     date = pd.Timestamp.now().date() - pd.Timedelta(days=1)
    #     store.put('last_update', date)

def save_all_trade_date():
    """保存所有交易日"""
    all_trade_date = ak.tool_trade_date_hist_sina()
    all_trade_date.to_csv(ALL_TRADE_DATE_PATH, index=False)

def save_stock_day(code="600000.SH",start_date = '20150101',end_date = ''):
    """
    保持股票日线数据(行情+利润表+财务指标)
    :param code: 股票代码
    :param start_date: 开始日期
    :param end_date: 结束日期
    """
    # 以下财务数据获取的是上一年的时间日期，之所以这样做是因为今年的1月1日在pro.fina_indicator函数里你是得不到1月1日这一天的财务数据的
    lastyear_date = datetime.strptime(start_date, '%Y%m%d') - timedelta(days=365)  # str转time
    fina_start_date = datetime.strftime(lastyear_date, '%Y%m%d')  # time转str
    # 获取每日数据
    df_daily = ts.pro_bar(ts_code=code, start_date=start_date, end_date=end_date, adj='qfq', freq='D')
    if df_daily is None:
        return 
    df_daily = df_daily.drop(['ts_code'], axis=1)
    # 获取每日基本指标数据
    df_stockind = pro.daily_basic(ts_code=code, start_date=start_date, end_date=end_date, adj='qfq',
                                    freq='D')
    df_stockind = df_stockind.drop(['ts_code','close'], axis=1)                             
    # 获取财务数据
    fina_columns = ['ann_date','eps', 'dt_eps', 'total_revenue_ps', 'revenue_ps', 'capital_rese_ps', 'surplus_rese_ps', 'undist_profit_ps', 'extra_item', 'profit_dedt', 'assets_turn', 'op_income', 'fcff', 'retained_earnings', 'diluted2_eps', 'bps', 'ocfps', 'retainedps', 'cfps', 'netprofit_margin', 'profit_to_gr', 'adminexp_of_gr', 'impai_ttm', 'op_of_gr', 'roe', 'roe_waa', 'roe_dt', 'npta', 'roe_yearly', 'debt_to_assets', 'assets_to_eqt', 'dp_assets_to_eqt', 'debt_to_eqt', 'eqt_to_debt', 'ocf_to_debt', 'roa_yearly', 'roa_dp', 'fixed_assets', 'profit_to_op', 'q_roe', 'q_dt_roe', 'q_npta', 'q_ocf_to_sales', 'basic_eps_yoy', 'dt_eps_yoy', 'cfps_yoy', 'op_yoy', 'ebt_yoy', 'netprofit_yoy', 'dt_netprofit_yoy', 'ocf_yoy', 'roe_yoy', 'bps_yoy', 'assets_yoy', 'eqt_yoy', 'tr_yoy', 'or_yoy', 'q_sales_yoy', 'q_op_qoq', 'equity_yoy']
    df_fina = pro.fina_indicator(ts_code=code, start_date=fina_start_date,fields=','.join(fina_columns))
    # 将ann_date列即公告日期（财务数据公布的那一天）更名，为后面数据合并提供依据,且减少数据处理
    df_fina = df_fina.rename(columns={'ann_date': 'trade_date'})
    # df_fina = df_fina[['trade_date', 'roe']]
    # df_fina = df_fina.drop(['ts_code',"end_date"], axis=1)
    # 获取财务数据所有字段除了trade_date
    fina_columns = df_fina.columns.tolist()
    fina_columns.remove('trade_date')
    # 获取净利润表
    income_columns = ['ann_date','report_type', 'comp_type', 'end_type', 'basic_eps', 'diluted_eps', 'total_revenue', 'revenue', 'int_income', 'comm_income', 'n_commis_income', 'n_oth_income', 'n_oth_b_income', 'oth_b_income', 'fv_value_chg_gain', 'invest_income', 'ass_invest_income', 'forex_gain', 'total_cogs', 'int_exp', 'comm_exp', 'biz_tax_surchg', 'admin_exp', 'assets_impair_loss', 'oper_exp', 'other_bus_cost', 'operate_profit', 'non_oper_income', 'non_oper_exp', 'total_profit', 'income_tax', 'n_income', 'n_income_attr_p', 'minority_gain', 'oth_compr_income', 't_compr_income', 'compr_inc_attr_p', 'compr_inc_attr_m_s', 'continued_net_profit', 'update_flag']
    df_income = pro.income(ts_code=code, start_date=fina_start_date,fields=','.join(income_columns))
    df_income = df_income.rename(columns={'ann_date': 'trade_date'})
    # df_income = df_income.drop(['ts_code',"f_ann_date","end_date","ebit","ebitda"], axis=1)
    # 转换 'report_type', 'comp_type', 'end_type'为整型
    # 如果 report_type 为 None 用整数99替换
    df_income['report_type'] = df_income['report_type'].fillna(99).astype(int)
    df_income['comp_type'] = df_income['comp_type'].fillna(99).astype(int)
    df_income['end_type'] = df_income['end_type'].fillna(99).astype(int)
    # 获取净利润表所有字段除了trade_date
    income_columns = df_income.columns.tolist()
    fina_columns.extend(income_columns)  # 将净利润表的字段加入到财务数据的字段中

    # 先合并每日数据跟每日基本指标数据
    df_all = pd.merge(left=df_daily, right=df_stockind, on='trade_date', how='outer') # outer是并集，inner是交集
    df_all = pd.merge(left=df_all, right=df_fina, on='trade_date', how='outer')
    df_all = pd.merge(left=df_all, right=df_income, on='trade_date', how='outer')

    df_all.set_index('trade_date', inplace=True)  # 设置索引覆盖原来的数据
    df_all = df_all.sort_index(ascending=True)  # 将时间顺序升序，符合时间序列

    # 使用向前填充缺失的数据，就是说假如000001.sz今天20200202公布了财务数据，ROE为8.544，那么明天20200203至到下一财务数据公布日都是8.544zzzzzzz
    fina_columns.remove('trade_date')  # 删除trade_date字段
    # print(fina_columns)
    for column in fina_columns:
        # if column == "continued_net_profit":
        #     print("xxxxxxxxxxxxxx")
        df_all[column].fillna(df_all[column].ffill(), inplace=True)
    df_all = df_all[df_all['close'].notna()]  # 删除停牌数据
    # 获取所有全列为NAN的字段
    # 取消trade_date索引
    df_all.reset_index(inplace=True)
    # 将trade_date列转换为yyyy-mm-dd格式
    df_all['trade_date'] = pd.to_datetime(df_all['trade_date'])
    # trade_date -> date
    df_all = df_all.rename(columns={'trade_date': 'date'})
    # code = change_code(code)
    # df_all.to_csv(f"{code}.csv",index=False)
    with pd.HDFStore(STOCK_DAY_PATH) as store:
        store.put(code, df_all, format='table',data_columns=True)
def save_all_stock_day():
    from data_helper.geter import get_all_stocks
    codes = get_all_stocks()
    progress_bar = tqdm(codes, desc="保存股票行情", unit=" 股票")
    for code in progress_bar:
        progress_bar.set_postfix(code=code)
        # code_ = change_code(code)
        # 如果已经存在则跳过
        with pd.HDFStore(STOCK_DAY_PATH) as store:
            if code in store:
                continue
        success = False
        while not success:
            try:
                save_stock_day(code)
                success = True
            except Exception as e:
                print(f"Error occurred for Stock {code}: {e}")
                time.sleep(5)  # 延迟5秒重试

def save_cb_day(code,stock_code,start_date="20150101",end_date="20230816"):
    from data_helper.geter import get_day
    # 1.获取转债日线行情 
    fields = ['ts_code', 'trade_date', 'pre_close', 'open', 'high', 'low', 'close', 'change', 'pct_chg', 'vol', 'amount','bond_value','bond_over_rate','cb_value','cb_over_rate']
    cb_df = pro.cb_daily(ts_code=code,start_date=start_date,end_date=end_date,fields=fields)
    if cb_df.empty:
        # 未获取到数据:未上市/
        return
    # 修改trade_date列名为date
    cb_df.rename(columns={"trade_date": "date"}, inplace=True)
    # 修改date列类型为datetime
    cb_df['date'] = pd.to_datetime(cb_df['date'])
    # 3.获取正股日线行情
    stock_df = get_day(stock_code,"stock",all=True)
    # 4.修改列名 open->open_stock,close->close_stock,high->high_stock,low->low_stock,vol->vol_stock,amount->amount_stock
    stock_df.rename(columns={"open": "open_stock", "close": "close_stock", "high": "high_stock", "low": "low_stock", "vol": "vol_stock", "amount": "amount_stock"}, inplace=True)
    # 5.合并转债日线行情和正股日线行情
    merged_df = pd.merge(cb_df, stock_df, on="date", how="outer")
    # 去除ts_code列
    merged_df.drop(columns=["ts_code"], inplace=True)
    # merged_df = merged_df[merged_df['close'].notna()]  # 删除停牌数据（使用层找不到数据要使用邻近算法）
    # 基于date列排序
    merged_df.sort_values("date", inplace=True)
    # 6.保存到hdf文件
    with pd.HDFStore(CB_DAY_PATH) as store:
        store.put(code, merged_df, data_columns=True,format="table")
    
def save_all_cb_day():
    from data_helper.geter import get_all_cb
    codes = get_all_cb(reture_stock=True)
    progress_bar = tqdm(codes, desc="保存所有可转债", unit=" 可转债")
    for code in progress_bar:
        progress_bar.set_description(f"保存 可转债 {code}")
        success = False
        with pd.HDFStore(CB_DAY_PATH) as store:
            if code[0] in store:
                continue
        while not success:
            try:
                save_cb_day(code[0],str(code[1]))
                success = True
            except Exception as e:
                print(f"Error occurred for CB {code}: {e}")
                time.sleep(5)
