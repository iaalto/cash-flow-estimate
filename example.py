import datetime
import cashflow


cf = cashflow.CashFlow('Example cash flow estimate')

#Generate data
cf.add_event('Original balance', 5000, datetime.date(2016, 5, 21))
cf.generate_series('Monthly salary', 1000, frequency='M', start=datetime.date(2016, 6, 1), end=datetime.date(2020,12,31))
cf.generate_series('Monthly rent and expenses', -600, frequency='MS', start=datetime.date(2016, 6, 1), end=datetime.date(2020,12,31))
cf.add_event('Car down payment', -3000, datetime.date(2016, 8, 20))
#First payment on 2016-09-01, beginning of month
cf.generate_series('Car loan amortization', -310, frequency='MS', start=datetime.date(2016, 8, 20), end=datetime.date(2020,12,31))
#First payment on 2017-01-01, beginning of year
cf.generate_series('Yearly car insurance payments', -400, frequency='AS', start=datetime.date(2016, 8, 20), end=datetime.date(2020,12,31))
#First payment on 2016-07-01, beginning of quarter
cf.generate_series('Quarterly dividends', 150, frequency='QS', start=datetime.date(2016, 5, 21), end=datetime.date(2020,12,31))

#Show the data
print(cf.series)
cf.export_to_csv('', 'example.csv')
cf.export_to_png('', 'example.png')
