import matplotlib.pyplot as plt
from matplotlib import dates

def plot_stock_data(y_data_array, x_data_array, name_of_file, labels=[]):
    plt.title('Price vs Day')
    plt.ylabel('Price')
    plt.xlabel('Day')
    plt.autoscale(axis='x',tight=False)
    for cnt, data in enumerate(y_data_array):
        try:
            plt.plot(x_data_array[cnt], data,label=labels[cnt])
        except:
            plt.plot(x_data_array[cnt], data, label=cnt)
    plt.xticks(rotation=45, fontsize=5)
    plt.savefig('output/results/graphs/' + name_of_file + '.png')