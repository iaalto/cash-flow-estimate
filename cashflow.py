import datetime
import pandas as pd
import csv
import os


class CashFlow(object):

    def __init__(self, name='cashflow'):
        self.name = name
        self.columns = ['date_of_activity', 'description', 'amount']
        self.series = pd.DataFrame(columns=self.columns)

    def generate_series(self, description, amount, frequency='MS',
                        start=datetime.date(datetime.date.today().year, 1, 1),
                        end=datetime.date(datetime.date.today().year, 12, 31)):
        """Generate a new data series and append it to the existing data"""
        data = [(date_of_activity, description, amount) for date_of_activity in pd.date_range(start, end, freq=frequency)]
        self.series = pd.concat([self.series, pd.DataFrame(data, columns=self.columns)])

    def add_event(self, description, amount, date_of_activity):
        """Add a single event"""
        self.generate_series(description, amount, frequency='D', start=date_of_activity, end=date_of_activity)

    def export_to_csv(self, dirpath, filename):
        """Export the data to a csv file

        Sort data by 1) date_of_activity ascending and 2) amount ascending before the export."""
        path = os.path.join(dirpath, filename)
        with open(path, 'w') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=';')
            csv_writer.writerow(self.columns)
            self.series.sort_values(by=['date_of_activity', 'amount'], ascending=[True, True], inplace=True)
            for index, record in self.series.iterrows():
                csv_writer.writerow(record)

    def export_to_png(self, dirpath, filename):
        """Export a graph representation of the data"""
        path = os.path.join(dirpath, filename)

        #Create auxiliary columns
        tmp = self.series.copy(deep=True)
        tmp['year'] = tmp['date_of_activity'].dt.year
        tmp['month'] = tmp['date_of_activity'].dt.month
        tmp['year_month'] = 100 * tmp['year'] + tmp['month']
        tmp['year'] = tmp['year'].map(str)
        tmp['year_month'] = tmp['year_month'].map(str)
        tmp['year_quarter'] = tmp['year'] + 'Q' + ((tmp['month'] - 1) // 3 + 1).map(str)

        #Create the graph on year, quarter or month level depending on date range
        months = (tmp['date_of_activity'].max() - tmp['date_of_activity'].min()).total_seconds() / (3600 * 24 * 30)
        xlabel = ''
        if months > 60:
            tmp = tmp.groupby(['year'], sort=True)['amount'].sum().cumsum()
            xlabel = 'Year'
        elif months > 20:
            tmp = tmp.groupby(['year_quarter'],sort=True)['amount'].sum().cumsum()
            xlabel = 'Quarter'
        else:
            tmp = tmp.groupby(['year_month'], sort=True)['amount'].sum().cumsum()
            xlabel = 'Month'

        plot = tmp.plot()
        plot.set_ylabel('Cumulative Amount')
        plot.set_xlabel(xlabel)
        fig = plot.get_figure()
        fig.savefig(path)
