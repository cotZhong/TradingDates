import numpy as np
import chinese_calendar
import datetime
import pandas as pd
from typing import List

class TradingDates():
    
    def __init__(
        self, 
        start_date = '2004-01-01', 
        end_date = '2024-12-31',
    ) -> None:
        
        self.trading_days = self._get_tradeday(start_date, end_date)
    
    @staticmethod
    def _get_tradeday(start_str, end_str):
        start = datetime.datetime.strptime(start_str, '%Y-%m-%d') # 将字符串转换为datetime格式
        end = datetime.datetime.strptime(end_str, '%Y-%m-%d')
        # 获取指定范围内工作日列表
        lst = chinese_calendar.get_workdays(start,end)
        expt = []
        # 找出列表中的周六，周日，并添加到空列表
        for time in lst:
            if time.isoweekday() == 6 or time.isoweekday() == 7:
                expt.append(time)
        # 将周六周日排除出交易日列表
        for time in expt:
            lst.remove(time)
        date_list = [item.strftime('%Y-%m-%d') for item in lst] #列表生成式，strftime为转换日期格式
        return date_list

    
    def backward(
        self, 
        now_day: str,
        days: int,
    ) -> str:
        """从now_day 倒退 days 个交易日"""
        if type(now_day) == pd._libs.tslibs.timestamps.Timestamp:
            now_day = datetime.datetime.strftime(now_day, '%Y-%m-%d')
        assert now_day in self.trading_days, '{} 不是交易日，或格式非标准'.format(now_day)
        idx = self.trading_days.index(now_day)
        assert 0 <= idx - days <= len(self.trading_days) - 1, '倒退出界'
        
        return self.trading_days[idx - days]
    
    def forward(
        self, 
        now_day: str,
        days: int,
    ) -> str:
        """从now_day 前进 days 个交易日"""
        if type(now_day) == pd._libs.tslibs.timestamps.Timestamp:
            now_day = datetime.datetime.strftime(now_day, '%Y-%m-%d')
        assert now_day in self.trading_days, '{} 不是交易日，或格式非标准'.format(now_day)
        idx = self.trading_days.index(now_day)
        assert 0 <= idx + days <= len(self.trading_days) - 1, '前进出界'
        
        return self.trading_days[idx + days]
    
    def date_delta(self, date1: str, date2:str) -> int:
        """Return date1 - date2的交易日天数"""
        assert (date1 in self.trading_days) and (date2 in self.trading_days), \
            'Please use trading days to run this date_delta'
        data1_loc = self.trading_days.index(date1)
        date2_loc = self.trading_days.index(date2)
        
        return data1_loc - date2_loc
    
    def next_trading_day(self, date: str) -> str:
        """date后的第一个交易日"""
        if date not in self.trading_days:
            tmp_trad_dates = np.array([
                datetime.datetime.strptime(x, '%Y-%m-%d') for x in self.trading_days
            ])
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            date = min(tmp_trad_dates[tmp_trad_dates >= date])
            date = datetime.datetime.strftime(date, '%Y-%m-%d')
        return date
    
    @staticmethod
    def sort(
        dates: List[str], 
        reverse: bool = False
    ) -> List[str]:
        """对时间序列排序
        :param dates: 日期列表
        :param reverse: False为升序排列, True为降序排列
        
        :return 排序后日期列表
        """
        dates = [
            datetime.datetime.strptime(x, '%Y-%m-%d') for x in dates
        ]
        dates.sort(reverse = reverse)
        dates = [
            datetime.datetime.strftime(x, '%Y-%m-%d') for x in dates
        ]
        return dates