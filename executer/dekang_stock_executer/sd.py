import os
import sys
import pandas as pd
# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取三级父目录的绝对路径
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(parent_dir)
import datetime
from executer.dekang_stock_executer.env import TradingEnv
from datetime import datetime, timedelta
from utils import Feature
from strategys.cb import TopFactor, ConditionedWarehouse
import os
import akshare as ak
import tushare as ts
import pandas as pd
from data_helper.common import STOCK_Trade_PATH
from utils import code_add_postfix
# from rocketry import Rocketry
# from rocketry.conditions.api import daily
ts.set_token('854634d420c0b6aea2907030279da881519909692cf56e6f35c4718c')
pro = ts.pro_api()

# app = Rocketry()


def get_price(code, start_date, end_date, frequency):
    # TODO: 封装
    pass


# @app.task(daily.after("14:55"))
# def task1():
#     # 获取000001.SZ的当前日线数据
#     df = get_price('000001.SZ', start_date=datetime.date.today(), end_date=datetime.date.today(), frequency='daily')
#     # 调用executer 获取账户信息
#     account_data = requests.post('http://127.0.0.1:8000/get_account')
#     # 调用wiser
def get_fin(ts_code,today):
    # 获取当日财务指标数据
    lastyear_date = datetime.strptime(today, '%Y%m%d') - timedelta(days=365)  # str转time
    fina_start_date = datetime.strftime(lastyear_date, '%Y%m%d')  # time转str
    # df_fina = pro.fina_indicator(ts_code=ts_code, start_date=fina_start_date)
    fina_columns = ['ann_date','end_date','eps', 'dt_eps', 'total_revenue_ps', 'revenue_ps', 'capital_rese_ps', 'surplus_rese_ps', 'undist_profit_ps', 'extra_item', 'profit_dedt', 'assets_turn', 'op_income', 'fcff', 'retained_earnings', 'diluted2_eps', 'bps', 'ocfps', 'retainedps', 'cfps', 'netprofit_margin', 'profit_to_gr', 'adminexp_of_gr', 'impai_ttm', 'op_of_gr', 'roe', 'roe_waa', 'roe_dt', 'npta', 'roe_yearly', 'debt_to_assets', 'assets_to_eqt', 'dp_assets_to_eqt', 'debt_to_eqt', 'eqt_to_debt', 'ocf_to_debt', 'roa_yearly', 'roa_dp', 'fixed_assets', 'profit_to_op', 'q_roe', 'q_dt_roe', 'q_npta', 'q_ocf_to_sales', 'basic_eps_yoy', 'dt_eps_yoy', 'cfps_yoy', 'op_yoy', 'ebt_yoy', 'netprofit_yoy', 'dt_netprofit_yoy', 'ocf_yoy', 'roe_yoy', 'bps_yoy', 'assets_yoy', 'eqt_yoy', 'tr_yoy', 'or_yoy', 'q_sales_yoy', 'q_op_qoq', 'equity_yoy']
    df_fina = pro.fina_indicator(ts_code=ts_code, start_date=fina_start_date,fields=','.join(fina_columns))
    
    return df_fina
# @app.task(daily.after("12:00"))
def get_caiwuzhibiao():
    """"""
    # 获取当前日期
    today = pd.Timestamp.today().strftime('%Y%m%d')
    # today = "20230928"
    today_datetime = datetime.strptime(today, '%Y%m%d')  # str转time
    df = ak.stock_zh_a_spot_em()
    columns = ["代码"]
    # rename
    df = df[columns]
    df.rename(columns={"代码": "code","最高":"high","最低":"low","今开":"open","最新价":"close","昨收":"pre_close","涨跌幅":"change","成交量":"vol","成交额":"amount"}, inplace=True)
    df['code'] = df['code'].apply(code_add_postfix)
    codes = df['code'].tolist()
    # 遍历分组
    merged_dfs = []
    for code in codes:
        # 获取当日财务指标数据
        df_fina = get_fin(code,today)
        df_fina["date"] = today_datetime
        df_fina["code"] = code
        # 合并
        merged_dfs.append(merged_df)
    # 合并所有
    merged_df = pd.concat(merged_dfs)
    # 写入当天行情
    parquet_name = f"{today}_fina.parquet"
    merged_df.to_parquet(os.path.join(STOCK_Trade_PATH,parquet_name), index=False)
# @app.task(daily.after("14:55"))
def get_hangqing():
    # 获取当前日期
    today = pd.Timestamp.today().strftime('%Y%m%d')
    # today = "20230928"
    df = ak.stock_zh_a_spot_em()
    columns = ["代码","最高","最低","今开","最新价","昨收","涨跌幅","成交量","成交额"]
    # rename
    df = df[columns]
    df.rename(columns={"代码": "code","最高":"high","最低":"low","今开":"open","最新价":"close","昨收":"pre_close","涨跌幅":"change","成交量":"vol","成交额":"amount"}, inplace=True)
    fina_parquet_name = f"{today}_fina.parquet"
    fina_df = pd.read_parquet(os.path.join(STOCK_Trade_PATH,fina_parquet_name))
    merged_df = pd.merge(df, fina_df, how="outer",on="code")
    parquet_name = f"{today}.parquet"
    merged_df = merged_df.dropna(subset='close')
    # 去除close为NaN的行
    merged_df.to_parquet(os.path.join(STOCK_Trade_PATH,parquet_name), index=False)

features = [
    Feature("close"),
    Feature("profit_to_gr"),
    Feature("dt_netprofit_yoy"),
    Feature("eqt_to_debt"),
    Feature("debt_to_assets"),
    Feature("roa_yearly"),
    Feature("q_npta"),
    Feature("npta"),
    Feature("roa_dp"),
    Feature("equity_yoy"),
]


strategy_pipelines = [
    # 选股
    TopFactor(
        factors=[

            {
                "name": "profit_to_gr",# # 新浪财经-财务分析-财务指标： stock_financial_analysis_indicator(总资产利润率(%))
                "big2smail": True,
            },
            {"name":"debt_to_assets","big2smail": True}, # stock_financial_analysis_indicator（资产负债率）
            
            {
                "name": "roa_yearly",
                "big2smail": True,
            },
            {
                "name": "debt_to_assets",
                "big2smail": True,
            },
            {"name": "eqt_to_debt","big2smail": False},
            {"name": "q_npta","big2smail": False},
            {"name": "roa_dp","big2smail": True,},
            {"name": "equity_yoy","big2smail": True,},
            
        ]
    ),
    # 调仓 
    ConditionedWarehouse(k=8),
]
# @app.task(daily.after("14:55"))
def jiaoyi():
    initial_balance = 100000 # TODO:获取当前资金
    position = dict()
    today = "20230928"
    # today = pd.Timestamp.today().strftime('%Y%m%d')
    data_path = os.path.join(STOCK_Trade_PATH,f"{today}.parquet")
    te = TradingEnv(
        features = features,
        strategy_pipelines = strategy_pipelines,
        initial_balance = initial_balance,
        breed="stock",
        position = position,
        data_path=data_path
    )
    output = te()
    print(output)
    # out 行为 (买/卖,什么,数量) 
    # 调用执行-TODO:是否在风险股票池（如聪明资金跑路，龙虎榜拉萨）
    pass
jiaoyi()