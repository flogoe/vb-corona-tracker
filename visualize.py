import argparse
import pandas as pd
import matplotlib.pyplot as plt
import re

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('logged_csv', type=str, help='CSV')
    parser.add_argument('--style', nargs=1, default='-', help='Plot line style')
    parser.add_argument('fields', metavar='field', nargs='*', help='REGEX')
    args = parser.parse_args()

    data = pd.read_csv(args.logged_csv, sep=';', index_col=0)
    if args.fields:
        regex_list = [re.compile(regex) for regex in args.fields]
        field_names = list(data)
        data_fields = list(filter(lambda field_name: any([True if regex.match(field_name) else False for regex in regex_list]), field_names))
        data = data[data_fields]
    fig, axes = plt.subplots()
    plot = data.plot(ax=axes, kind='line', style=args.style, use_index=True)
    plt.show()

if __name__ == '__main__':
    main()