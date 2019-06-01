from statsmodels.graphics.mosaicplot import mosaic
import matplotlib.pyplot as plt
import pandas as pd

data_path = "./../../data/data.csv"

def plot_mosaic_education():
    data = pd.read_csv(data_path)
    data = data[data['EDUCATION'] != 0]
    data = data[data['EDUCATION'] != 5]
    data = data[data['EDUCATION'] != 6]
    
    mosaic(data.sort_values('EDUCATION'), ['EDUCATION', 'default payment next month'])
    plt.show()

def print_target_balance():
    data = pd.read_csv(data_path)
    target = data['default payment next month']
    balance = target.value_counts()
    print(balance)

if __name__ == "__main__":
    print_target_balance()