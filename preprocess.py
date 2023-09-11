import os
import pandas as pd
import mplfinance as mpf
from pathlib import Path


def read_csv_files(directory):
    files = []
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            files.append(os.path.join(directory, file))
    return files


def gen_hma(input_dir="", output_dir="", Ns=[17, 50, 138, 556]):
    # Create a directory named "df" in the output directory if it doesn't already exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Loop through each file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            # Read in the CSV file
            input_path = os.path.join(input_dir, filename)
            df = pd.read_csv(input_path)

            # Calculate the HMA values and add them to the DataFrame
            for N in Ns:
                prev_hma = None
                col_name = f'HMA{N}'
                for i, row in df.iterrows():
                    close = row['Close']
                    if i == 0:
                        hma = close
                    else:
                        if prev_hma is None:
                            prev_hma = df.at[i - 1, col_name]
                        hma = close * 2 / (N + 1) + prev_hma * (N - 1) / (N + 1)
                    df.at[i, col_name] = hma
                    prev_hma = hma

            # Save the new CSV file to the "df" directory with the same name as the input file
            output_path = os.path.join(output_dir, filename)
            df.to_csv(output_path, index=False)
    notification = f"HMA generation Completed."
    return notification, output_dir


def preprocess(input_dir: str, output_dir: str, _gen_hma: bool):
    csv_files = read_csv_files(input_dir)
    output_data_dir = output_dir
    Path(output_data_dir).mkdir(parents=True, exist_ok=True)

    for file in csv_files:
        df = pd.read_csv(file)
        df['MA5'] = df['close'].rolling(window=5).mean()
        df['MA25'] = df['close'].rolling(window=25).mean()
        df['MA60'] = df['close'].rolling(window=60).mean()
        df['MA99'] = df['close'].rolling(window=99).mean()
        df.rename(
            columns={'date': 'Date', 'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low',
                     'volume': 'Volume',
                     'code': 'Code'}, inplace=True)
        df.index = pd.DatetimeIndex(df.index)
        df.index.name = 'Date'
        if "name" in df.columns:
            df = df.drop('name', axis=1)
        df = df.iloc[99:]
        file_name = os.path.splitext(os.path.basename(file))[0]
        output_csv_path = os.path.join(output_data_dir, f"{file_name}.csv")
        df.to_csv(output_csv_path, index=False, encoding='utf8')

    if _gen_hma:
        notification, input_dir = gen_hma(output_data_dir, output_data_dir)
        print(notification)
    else:
        notification, input_dir = ("HMA already exists.", os.path.join(output_dir, 'df'))
        print(notification)



