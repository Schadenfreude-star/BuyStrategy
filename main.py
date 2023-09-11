from preprocess import preprocess
from strategy import Strategy, Strategy_2

from constants import *

input_directory = r'E:\LabFiles\毕设\target_signal\匹配结果\2'
output_directory = r'E:\LabFiles\毕设\target_signal\匹配结果\2\processed'
file_type = "csv"
labels = ['MA60']
_gen_hma = True


def main():
    # preprocess(input_directory, output_directory, _gen_hma)
    strategy_1 = Strategy(output_directory, file_type, signal_2)
    # strategy_2 = Strategy_2(output_directory, file_type, signal_1)

    avg_rates = strategy_1.apply_strategy(labels)
    # avg_rates = strategy_2.apply_strategy(labels)
    print(avg_rates)
    avg_rate = 0
    for record in avg_rates:
        avg_rate += record["gain_rate"]
    print(avg_rate / len(avg_rates))


if __name__ == '__main__':
    main()
