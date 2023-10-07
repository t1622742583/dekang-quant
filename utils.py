
from typing import List
import numpy as np
import pandas as pd
MAX_INT = np.iinfo(np.int32).max
MAX_SHARE_PRICE = 3000 # 最大股价
MAX_VOLUME = 1000e8  # 最大成交量
MAX_AMOUNT = 3e10  # 最大成交额
MAX_ACCOUNT_BALANCE = MAX_INT  # 最大账户余额
MAX_NUM_SHARES = 2147483647  # 最大持仓数量
MAX_OPEN_POSITIONS = 5  # 最大持仓数量
MAX_STEPS = 20000  # 最大步数
MAX_DAY_CHANGE = 1  # 最大日涨幅
class Feature:
    def __init__(self, name, build=None, normalization=None):
        """
        :param name: 字段名称
        :param build: 构建方案
        :param normalization: 标准化方案
        """
        self.name = name
        self.build = build
        self.normalization = normalization

    def __call__(self, now_market,date=None):
        codes = now_market.index.values
        if self.build:
            value = self.build(self.name, codes, date, now_market)
        else:
            value = now_market[self.name]
        if self.normalization:
            value = self.normalization(value)
        return value
class NormalPrice:
    def __init__(self, max_price=MAX_SHARE_PRICE):
        self.max_price = max_price

    def __call__(self, price):
        return price / self.max_price
class NormalVolume:
    def __init__(self, max_volume=MAX_VOLUME):
        self.max_volume = max_volume

    def __call__(self, volume):
        return volume / self.max_volume
    

# 股价
class Analyzer:
    # TODO: 画基准线
    def __init__(self, df_results: pd.DataFrame, benchmarks: List[str] = ['000300.SH']):
        self.df_results = df_results
        self.benchmarks = benchmarks

    def show_results(self):
        returns = self.df_results['rate']
        import empyrical
        print('累计收益：', round(empyrical.cum_returns_final(returns), 3))
        print('年化收益：', round(empyrical.annual_return(returns), 3))
        print('最大回撤：', round(empyrical.max_drawdown(returns), 3))
        print('夏普比', round(empyrical.sharpe_ratio(returns), 3))
        print('卡玛比', round(empyrical.calmar_ratio(returns), 3))
        print('omega', round(empyrical.omega_ratio(returns)), 3)

    def plot(self):
        returns = []

        se_port = self.df_results['rate']
        se_port.name = '策略'
        returns.append(se_port)
        all_returns = pd.concat(returns, axis=1)
        all_returns.dropna(inplace=True)
        all_equity = (1 + all_returns).cumprod()

        import matplotlib.pyplot as plt
        all_equity.plot()
        plt.show()

def change_code(code):
    if code.endswith(".SH"):
        code = code.replace(".SH","")
        code = "sh"+code
    elif code.endswith(".SZ"):
        code = code.replace(".SZ","")
        code = "sz"+code
        
    return code
def code_add_postfix(code):
    """给code加上后缀"""
    if code.startswith("6"):
        code = code + ".SH"
    elif code.startswith("0") or code.startswith("3"):
        code = code + ".SZ"
    else:
        code = code + ".BJ"
    return code