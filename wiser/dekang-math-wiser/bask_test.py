import os
import sys

# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取三级父目录的绝对路径
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(parent_dir)

import pandas as pd
from utils import Feature
from typing import List

from data_helper.geter import get_all_day, get_trade_days
breed_unit = {
    "cb": 10,
    "stock": 100,
}
class Account:
    def __init__(self,
                 init_cash: float = 100000,  # 初始资金
                 commission: float = 0.0003,  # 手续费
                 stamp_duty: float = 0.001,  # 印花税
                 breed: str = "cb",  # 品种
                 ):
        self.breed = breed
        self.init_cash = init_cash  # 初始资金
        self.curr_cash = self.init_cash  # 当前现金
        self.now_net_worth = self.init_cash  # 当前净值
        self.commission = commission  # 手续费
        self.stamp_duty = stamp_duty  # 印花税
        self.cache_net_worth = []  # 每日市值序列
        self.cache_position = []   # 每日持仓序列
        self.position = {}  # 持仓 {"code": {"price": 100.0, "shares": 100}}

    @property
    def profit(self):
        """收益"""
        return self.now_net_worth - self.init_cash
    def update_net_worth(self):
        """更新净值"""
        self.now_net_worth = self.curr_cash + sum([self.position[code]["shares"] * breed_unit[self.breed] * self.position[code]["price"]  for code in self.position.keys()])
    def change_position(self, selected_codes: List[dict]):
        # 传入 [{'code': 'sz123011', 'price': 95.913, 'ratio': 0.1}, {'code': 'sz123010', 'price': 91.495, 'ratio': 0.1}, {'code': 'sz123002', 'price': 105.92, 'ratio': 0.1}, {'code': 'sz128044', 'price': 94.711, 'ratio': 0.1}, {'code': 'sh113505', 'price': 90.62, 'ratio': 0.1}, {'code': 'sz128037', 'price': 87.876, 'ratio': 0.1}, {'code': 'sz123012', 'price': 93.41, 'ratio': 0.1}, {'code': 'sh110048', 'price': 104.19, 'ratio': 0.1}, {'code': 'sh110044', 'price': 99.6, 'ratio': 0.1}, {'code': 'sh110047', 'price': 99.36, 'ratio': 0.1}]
        # 先卖后调，如果当前持仓不在选股范围，获取当前收盘价价格清仓，去除仓位key，现金余额增加
        # 1.获取当前持仓
        curr_holding = self.position.keys()
        # 2.获取当前选股
        s_codes = [item["code"] for item in selected_codes]
        # 3.获取需要卖出的股票
        sell_codes = set(curr_holding) - set(s_codes)
        # 5.卖出
        for code in sell_codes:
            code_info = self.position[code]
            add_cash = code_info["shares"] * breed_unit[self.breed] * code_info["price"] * (1 - self.commission - self.stamp_duty)
            self.position.pop(code)
            self.curr_cash += add_cash
        # a.先处理减仓，基于调仓比例计算相应手数，不同于加仓 不足10手按10手计算，“优减”，调整仓位key值，现金数增加
        # 更新市值
        self.update_net_worth()
        trade_share = {}
        for selected_code in selected_codes.copy():
            code = selected_code["code"]
            # if code in self.position.keys():
            shares = selected_code["ratio"] * self.now_net_worth / (selected_code["price"]*breed_unit["cb"])
            if shares < 1:
                selected_codes.remove(selected_code)
                continue
            shares = int(shares)
            trade_share[code] = shares
        add_trade_share = {}
        for code in trade_share.keys():
            if code in self.position.keys():
                if trade_share[code] < self.position[code]["shares"]:
                    # 减仓
                    self.position[code]["shares"] = trade_share[code]
                    # 余额增加
                    add_cash = (self.position[code]["shares"] - trade_share[code]) * self.position[code]["price"] *breed_unit[self.breed]* (1 - self.commission - self.stamp_duty)
                    self.curr_cash += add_cash
                elif trade_share[code] == self.position[code]["shares"]:
                    # 不变
                    continue
                else:
                    # 大于 加仓 等于 不变
                    add_trade_share[code] = trade_share[code] - self.position[code]["shares"]
            else:
                add_trade_share[code] = trade_share[code]
        # 加仓
        for code in add_trade_share.keys():
            # 买入
            # 原始手数+add_trade_share[code]
            if code in self.position.keys():
                self.position[code]["shares"] += add_trade_share[code]
            else:
                self.position[code] = {"price": selected_code["price"], "shares": add_trade_share[code]}
            # 余额减少
            self.curr_cash -= add_trade_share[code] * breed_unit[self.breed] * selected_code["price"] * (1 + self.commission)

        # 更新市值
        self.update_net_worth()
        # 保存当前持仓
        self.cache_position.append(self.position)
        # 保存当前市值
        self.cache_net_worth.append(self.now_net_worth)


class TradingEnv():
    """交易环境"""

    def __init__(self,
                 start_date: str,  # 开始日期
                 end_date: str,  # 结束日期
                 features: List,  # 特征列表
                 initial_balance: float = 100000,  # 初始账户余额
                 commission: float = 0.0003,
                 stamp_duty: float = 0.001,  # 印花税 千1
                 strategy_pipelines: List = None,  # 策略流水线
                 breed: str = "cb",  # 品种 
                 run_mode:str = "day" # 运行模式 ["day","month","year"]
                 ):
        super(TradingEnv, self).__init__()  # 父类初始化
        self.run_mode = run_mode
        self.account = Account(init_cash=initial_balance, commission=commission, stamp_duty=stamp_duty)  # 账户
        self.start_date = start_date  # 开始日期
        self.end_date = end_date  # 结束日期
        self.initial_balance = initial_balance  # 初始账户余额
        self.features = features  # 特征列表
        self.strategy_pipelines = strategy_pipelines  # 策略管道
        self.trade_days = get_trade_days(self.start_date, self.end_date)
        self.selected_codes = []  # 选中的股票/可转债代码
        # 获取交易时间内所有行情
        self.codes,self.market_df = get_all_day(breed=breed,use_cache=True)
        self.market_df = self.market_df[self.market_df['close'].notna()]  # 删除停牌数据
    def get_current_observation(self):
        self.current_observation_df = self.market_df[self.market_df["date"]==self.current_date]
        self.current_observation_df.set_index("code",inplace=True)
        feature_dict = {}
        for feature in self.features:
            feature_dict[feature.name] = feature(self.current_observation_df)
        self.current_observation_df = pd.DataFrame(feature_dict)
    def step(self):
        """执行一步"""
        # 获取当前观察值
        self.get_current_observation()
        # 1.获取账户中所有持仓
        # 2.基于持仓标的获取当前收盘价
        # 3.更新当前市值
        codes = self.account.position.keys()
        for code in codes:
            # 2.1获取当前收盘价
            close = self.current_observation_df.loc[code,"close"]
            # 2.2更新持仓价格
            self.account.position[code]["price"] = close
        # 执行策略流水线
        for strategy_pipeline in self.strategy_pipelines:
            strategy_pipeline(self)
        # TODO:执行调仓 [{"code":str."ratio":float,"price":float"}"}]
        self.account.change_position(self.selected_codes)


    def run(self):
        """运行"""
        for i,trade_date in enumerate(self.trade_days):
            self.current_date = trade_date
            # TODO:根据run_mode跳过
            if i % 5 != 0:
                continue
            self.step()
            print(f"第{i}天，{trade_date}，{self.account.now_net_worth}")
            pass
        # TODO:总结
        pass


features = [
    Feature("close"),
    Feature("cb_over_rate"),
    Feature("profit_to_gr"),
    Feature("dt_netprofit_yoy"),
]
from strategys.cb import TopFactor, ConditionedWarehouse

strategy_pipelines = [
    # 选股
    TopFactor(
        factors=[
            {
                "name": "cb_over_rate",
                "big2smail": True,
            },
            {
                "name": "profit_to_gr",
                "big2smail": True,
            },
            {
                "name": "dt_netprofit_yoy",
                "big2smail": False,
            }
        ]
    ),
    # 调仓
    ConditionedWarehouse(k=10),
]
TradingEnv(start_date="2019-01-01", end_date="2020-01-01", features=features,
           strategy_pipelines=strategy_pipelines).run()
# 先尝试固定仓位，再尝试动态仓位
