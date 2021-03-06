import matplotlib
matplotlib.use('TKAgg') 

import argparse
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import copy
from data import loader

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform some SL experiments')
    parser.add_argument('--steel', action='store_true', help='Analyze steel plate fault dataset')
    parser.add_argument('--rain', action='store_true')
    parser.add_argument('--skyserver', action='store_true')
    parser.add_argument('--credit_default', action='store_true')
    parser.add_argument('--kde', action='store_true', default=True, help='Map the lower triangle to a distribution')
    parser.add_argument('--file', type=str, default="output.png")
    parser.add_argument('--samples', type=int, default=1000, help='Samples the dataset which may speed things up:')
    parser.add_argument('--verbose', '-v', action='store_true', default=True)
    args = parser.parse_args()
    verbose = args.verbose

all_sets = []
if args.steel:
    keep = ['0', '2', '8', '13', '33']
    log = ['13', '0']
    dataset = loader.SteelPlateData(verbose=args.verbose, binarize=True)
    dataset.load_and_process()
    dataset._data = dataset._data[keep]
    dataset._data[log] = np.log(dataset._data[log])


    all_sets.append(dataset)

if args.rain:
    keep = ['MinTemp', 'Sunshine', 'WindSpeed3pm', 'Humidity3pm', 'RainToday', 'RainTomorrow']
    dataset = loader.AusWeather(verbose=args.verbose)
    dataset.load_and_process()
    dataset._data = dataset._data[keep]
    all_sets.append(dataset)

if args.credit_default:
    dataset = loader.CreditDefaultData(verbose=args.verbose)
    dataset.load_and_process()
    all_sets.append(dataset)

if args.skyserver:
    keep = ['g', 'dec', 'field', 'redshift', 'ra', 'class']

    dataset = loader.SkyServerData(verbose=args.verbose)
    dataset.load_and_process()
    dataset._data = dataset._data[keep]
    all_sets.append(dataset)


if args.kde:
    diag = 'kde'
else:
    diag = 'hist'

all_grids = []
for data in all_sets:
    # Grab class name from the dataset
    # TODO This won't work with onehot classes (just because I don't need it)
    # SO have solved this problem though
    if data._data.shape[0] < args.samples:
        samples = data._data.shape[0]
    else:
        samples = args.samples
    classname = data.class_column_name()
    # Grab all data except the end which is the class label.
    grid = sns.pairplot(data._data.sample(args.samples), hue=classname,
                        vars=data._data.keys()[:-1],
                        diag_kind=diag, plot_kws={'s': 10}, size = 2.5)
    grid.map_lower(sns.kdeplot)
    grid.savefig("{}.png".format(data.data_name()))