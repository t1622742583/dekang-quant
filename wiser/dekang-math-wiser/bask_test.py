import os
import sys
from loguru import logger
import pandas as pd
# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取三级父目录的绝对路径
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(parent_dir)
from utils import Analyzer, Feature
from typing import List

from data_helper.geter import get_all_day, get_custom_day, get_trade_days
breed_unit = {
    "cb": 10,
    "stock": 100,
}
class Account:
    def __init__(self, init_cash: float = 100000, commission: float = 0.0003, stamp_duty: float = 0.001, breed: str = "cb"):
        self.breed = breed
        self.init_cash = init_cash
        self.curr_cash = self.init_cash
        self.now_net_worth = self.init_cash
        self.commission = commission
        self.stamp_duty = stamp_duty
        self.cache_net_worth = []
        self.cache_position = []
        self.position = {}
        self.unit = breed_unit[self.breed]

    @property
    def profit(self):
        return self.now_net_worth - self.init_cash

    def update_net_worth(self):
        self.now_net_worth = self.curr_cash + sum([self.position[code]["shares"] * self.unit * self.position[code]["price"] for code in self.position.keys()])
        # 保留2位小数
        self.now_net_worth = round(self.now_net_worth,2)

    def change_position(self, selected_codes: List[dict]):
        # Create a copy of the current position dictionary
        prev_position = self.position.copy()

        # Sell positions not in the selected codes list
        for code in prev_position.keys():
            if code not in [code_info["code"] for code_info in selected_codes]:
                self.sell_position(code)

        # Update the position for each selected code
        for code_info in selected_codes:
            code = code_info["code"]
            price = code_info["price"]
            conversion_ratio = code_info["ratio"]

            if code in prev_position:
                prev_shares = prev_position[code]["shares"]
                shares_diff = prev_shares - int(self.now_net_worth * conversion_ratio / (price * self.unit))
                shares_diff = int(shares_diff)
                if shares_diff > 0:
                    # Sell a portion of the position
                    shares_to_sell = shares_diff
                    self.sell_position(code, shares_to_sell)
                elif shares_diff < 0:
                    # buy a portion of the position
                    self.buy_position(code, price, -shares_diff)
                    
            else:
                # Buy the position
                shares = self.now_net_worth * conversion_ratio / (price * self.unit)
                shares = int(shares)
                self.buy_position(code, price, shares)

        # Update the net worth
        self.update_net_worth()
        self.cache_net_worth.append(self.now_net_worth)

    def sell_position(self, code: str, shares: int = None):
        if code in self.position:
            if shares is None:
                shares = self.position[code]["shares"]

            price = self.position[code]["price"]

            # Calculate the sale amount
            sale_amount = shares * self.unit * price

            # Calculate the transaction costs
            commission = sale_amount * self.commission
            # 保留2位小数
            commission = round(commission,2)
            stamp_duty = sale_amount * self.stamp_duty
            stamp_duty = round(stamp_duty,2)

            # Update the current cash and net worth
            self.curr_cash += sale_amount - commission - stamp_duty
            self.update_net_worth()

            # Remove the position from the dictionary if all shares are sold
            if shares == self.position[code]["shares"]:
                del self.position[code]
            else:
                # Update the shares in the position dictionary
                self.position[code]["shares"] -= shares

    def buy_position(self, code: str, price: float, shares: int):
        # Calculate the purchase amount
        purchase_amount = shares * self.unit * price

        # Calculate the transaction costs
        commission = purchase_amount * self.commission
        commission = round(commission,2)
        # Check if the current cash is sufficient for the purchase
        if purchase_amount + commission > self.curr_cash:
            print("Insufficient funds to buy the position.")
            return

        # Update the current cash and net worth
        self.curr_cash -= purchase_amount + commission 

        self.update_net_worth()
        # Add the position to the dictionary
        if code not in self.position:
            self.position[code] = {"price": price, "shares": shares}
        else:
            self.position[code]["shares"] += shares

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
                 ,load_custom_data:bool = False # 是否加载自定义数据
                 ,custom_data_path:str = None # 自定义数据路径
                 ,step_days:int = None # 步长
                 ,loging_day:bool = False # 是否打印日志
                 ):
        super(TradingEnv, self).__init__()  # 父类初始化
        self.loging_day = loging_day
        if step_days is not None:
            self.step_days = step_days
        else:
            self.run_mode = run_mode
            if self.run_mode == "day":
                self.step_days = 1
            elif self.run_mode == "week":
                self.step_days = 7
            elif self.run_mode == "month":
                self.step_days = 30
            elif self.run_mode == "year":
                self.step_days = 365
    
        self.account = Account(init_cash=initial_balance, commission=commission, stamp_duty=stamp_duty)  # 账户
        self.start_date = start_date  # 开始日期
        self.end_date = end_date  # 结束日期
        self.initial_balance = initial_balance  # 初始账户余额
        self.features = features  # 特征列表
        self.strategy_pipelines = strategy_pipelines  # 策略管道
        self.trade_days = get_trade_days(self.start_date, self.end_date)
        self.selected_codes = []  # 选中的股票/可转债代码
        # 获取交易时间内所有行情
        if load_custom_data:
            self.codes,self.market_df = get_custom_day(data_path=custom_data_path)
        else:
            self.codes,self.market_df = get_all_day(breed=breed,cache=True)
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
        trade_dates = []
        for i,trade_date in enumerate(self.trade_days):
            self.current_date = trade_date
            # TODO:根据run_mode跳过
            if i % self.step_days != 0:
                continue
            trade_dates.append(trade_date)
            self.step()
            if self.loging_day:
                logger.info(f"第{i}天，{trade_date}，{self.account.now_net_worth}，当前持仓{self.account.position}")
            pass
        # TODO:总结 
        # df_results = pd.DataFrame({"rate":self.account.cache_net_worth,"date":trade_dates})
        # analyzer = Analyzer(df_results=df_results)
        # analyzer.plot()
        # analyzer.show_results()


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
    ConditionedWarehouse(k=25),
]
TradingEnv(
    start_date="2019-01-01",
    end_date="2023-08-15",
    features=features,
    strategy_pipelines=strategy_pipelines,
    run_mode="week",
    loging_day=True
        ).run()

