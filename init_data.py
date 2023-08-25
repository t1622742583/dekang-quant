from loguru import logger
import argparse
import os


def main(opt):
    # 检查文件夹是否存在
    if not os.path.exists('data'):
        # 创建文件夹
        os.makedirs('data')
        
    if opt.breed == '':
        logger.error("请输入相应品种: python init_data.py -b etf/stock/cb")
    if opt.breed == "etf":
        pass
    elif opt.breed == "stock":
        from data_helper.saver import save_all_stock_day
        save_all_stock_day()
    elif opt.breed == "cb":
        from data_helper.saver import save_all_cb_day
        save_all_cb_day()
    elif opt.breed == "trade_date":
        from data_helper.saver import save_all_trade_date
        save_all_trade_date()
    else:
        logger.error("请输入正确的品种: python init_data.py -b etf/stock/cb")
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--breed', type=str, default='cb', help='下载行情品种：etf/stock/cb ')
    opt = parser.parse_args()
    main(opt)