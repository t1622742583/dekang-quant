import akshare as ak
import tushare as ts
import pandas as pd
from tqdm import tqdm
from data_helper.common import BREAD_PATH, CACHE_DAY_PATH
from data_helper.geter import get_all_day
pd.set_option('expand_frame_repr', False)  # True就是可以换行显示。设置成False的时候不允许换行
pd.set_option('display.max_columns', None)  # 显示所有列
# pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('colheader_justify', 'centre')  # 显示居中
ts.set_token('854634d420c0b6aea2907030279da881519909692cf56e6f35c4718c')
# #  初始化pro接口
pro = ts.pro_api()
df = pro.top_inst(trade_date='20230919')
df = df[df['net_buy'] > 0]
poss = ['中信证券股份有限公司北京望京证券营业部', '湘财证券股份有限公司上海泰兴路证券营业部', '华泰证券股份有限公司深圳留仙大道众冠大厦证券营业部', '华宝证券有限责任公司福州八一七北路证券营业部', '湘财证券\
股份有限公司义乌篁园路证券营业部', '申银万国证券股份有限公司上海斜土路证券营业部', '开源证券股份有限公司重庆分公司', '湘财证券股份有限公司郴州青年大道证券营业部', '华泰证券股份有限公司上海浦东新区乳\
山路证券营业部', '财通证券股份有限公司无锡政和大道证券营业部', '方正证券股份有限公司厦门厦禾路证券营业部', '华宝证券有限责任公司杭州玉古路证券营业部', '财达证券有限责任公司石家庄新华路证券营业部'] 
negs = []
poss_codes = []
negs_codes = []
exalters = df['exalter'].unique().tolist()
for exalter in exalters:
    if exalter in negs_codes:
        codes = df[df['exalter'] == exalter]['ts_code'].tolist()
        negs_codes.extend(codes)
negs_codes = list(set(negs_codes))
for exalter in exalters:
    if exalter in poss_codes:
        codes = df[df['exalter'] == exalter]['ts_code'].tolist()
        for code in codes:
            if code in negs_codes:
                continue
            poss_codes.append(code)
poss_codes = list(set(poss_codes))
print(f"poss_codes:{len(poss_codes)}")
print(f"negs_codes:{len(negs_codes)}")