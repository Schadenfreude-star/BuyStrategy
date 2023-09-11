import os
from enum import Enum

import pandas as pd


class FileType(Enum):
    csv = "csv"
    xls = "xls"
    xlsx = "xlsx"


def get_signal_by_name(name, signals):
    for signal in signals:
        if signal in name:
            time = signals[signal]
            return signal, time


class Strategy:
    def __init__(self, input_dir, file_type, signals):
        self.input_dir = input_dir
        self.file_type = file_type
        self.signals = signals

    def gen_df_by_name(self, name, filetype):
        if filetype in FileType._value2member_map_:
            if filetype == FileType.csv.value:
                try:
                    path = os.path.join(self.input_dir, name) + "." + filetype
                    return pd.read_csv(path, encoding="utf8")
                except FileExistsError:
                    return "DO NOT HAVE THIS FILE!"

            if filetype == FileType.xls.value:
                ...

            if filetype == FileType.xlsx.value:
                ...

        else:
            return "DO NOT SUPPORT THIS FILE TYPE!"

    def get_df_after_signal_by_date(self):
        files = iter([file for file in os.listdir(self.input_dir) if file.endswith("." + self.file_type)])
        if self.file_type == FileType.csv.value:
            for file in files:
                name, filetype = file.split(".")
                signal_name, signal_time = get_signal_by_name(name, self.signals)
                df = self.gen_df_by_name(name, filetype)
                index_value = df[df['Date'] == signal_time].index[0]
                df_after_signal = df.iloc[index_value:]
                yield df_after_signal

    def apply_strategy(self, indicators):
        res = []
        df_after_signal_generator = self.get_df_after_signal_by_date()
        for df_after_signal in df_after_signal_generator:
            result = {
                "name": ...,
                "sell_price": ...,
                "buy_price": ...,
                "sell_date": ...,
                "buy_date": ...,
                "gain": ...,
                "gain_rate": ...,
            }
            indicator_1 = indicators[0]
            buy_point = df_after_signal.iloc[0]
            df_after_signal.loc[:, "MA60_delta"] = df_after_signal.loc[:, indicator_1].diff()
            potential_sell_point = df_after_signal.loc[df_after_signal["MA60_delta"] < 0].head(1).iloc[0]
            meet_point = df_after_signal.loc[df_after_signal['Close'] > buy_point.Close * 1.15].head(1)
            if meet_point.empty:
                sell_point = potential_sell_point
            else:
                meet_point = meet_point.iloc[0]  # 想不出其他实现方式了
                if meet_point.Date < potential_sell_point.Date:
                    sell_point = meet_point
                else:
                    sell_point = potential_sell_point

            gain = sell_point.Close - buy_point.Close
            gain_rate = gain / buy_point.Close

            result["buy_price"] = buy_point.Close
            result["sell_price"] = sell_point.Close
            result["buy_date"] = buy_point.Date
            result["sell_date"] = sell_point.Date
            result["gain"] = gain
            result["name"] = buy_point.Code
            result["gain_rate"] = gain_rate
            res.append(result)

        print("STRATEGY APPLIED!")
        return res


class Strategy_2(Strategy):
    def apply_strategy(self, indicators):
        res = []
        df_after_signal_generator = self.get_df_after_signal_by_date()
        for df_after_signal in df_after_signal_generator:
            result = {
                "name": ...,
                "sell_price": ...,
                "buy_price": ...,
                "sell_date": ...,
                "buy_date": ...,
                "gain": ...,
                "gain_rate": ...,
            }
            indicator_1 = indicators[0]
            buy_point = df_after_signal.iloc[0]
            sell_point = df_after_signal.iloc[0 + 50]

            gain = sell_point.Close - buy_point.Close
            gain_rate = gain / buy_point.Close

            result["buy_price"] = buy_point.Close
            result["sell_price"] = sell_point.Close
            result["buy_date"] = buy_point.Date
            result["sell_date"] = sell_point.Date
            result["gain"] = gain
            result["name"] = buy_point.Code
            result["gain_rate"] = gain_rate
            res.append(result)

        print("STRATEGY APPLIED!")
        return res
