import datetime

from unittest import TestCase
from cashflow import CashFlow
from testfixtures import TempDirectory


class CashFlowTest(TestCase):
    def setUp(self):
        self.cashflow = CashFlow('test')

    def testEmptyCashFlow(self):
        self.assertTrue(self.cashflow.series.empty)

    def testGenerateFullYearSeries(self):
        """Default series has monthly frequency for the current year"""
        self.cashflow.generate_series('Salary', 1000)
        self.assertEquals(1000 * 12, self.cashflow.series["amount"].sum())

    def testGenerateNegativeSeries(self):
        self.cashflow.generate_series('Rent', -500)
        self.assertEquals(-500 * 12, self.cashflow.series["amount"].sum())

    def testGeneratePartialYearSeries(self):
        """Default series runs on monthly frequency until the end of the current year"""
        self.cashflow.generate_series('Salary', 1000, start=datetime.date(datetime.date.today().year, 3, 1))
        self.assertEquals(1000 * 10, self.cashflow.series["amount"].sum())

    def testGenerateTwoSeries(self):
        self.cashflow.generate_series('Salary', 1000)
        self.cashflow.generate_series('Rent', -500)
        self.assertEquals(1000 * 12 + (-500) * 12, self.cashflow.series["amount"].sum())

    def testGenerateOneDaySeries(self):
        self.cashflow.generate_series('Salary', 1000, start=datetime.date(2016, 3, 1), end=datetime.date(2016, 3, 1))
        self.assertEquals(1000, self.cashflow.series["amount"].sum())

    def testGenerateEmptySeries(self):
        """By default frequency is month start so no series would be returned for this date range"""
        self.cashflow.generate_series('Salary', 1000, start=datetime.date(2016, 3, 2), end=datetime.date(2016, 3, 31))
        self.assertTrue(self.cashflow.series.empty)

    def testGenerateOverOneYearSeries(self):
        """Default series runs on monthly frequency from the beginning of the current year"""
        self.cashflow.generate_series('Salary', 1000, end=datetime.date(datetime.date.today().year + 4, 12, 31))
        self.assertEquals(5 * (1000 * 12), self.cashflow.series["amount"].sum())

    def testAddEvent(self):
        self.cashflow.add_event('Original Balance', 5200, datetime.date(2015, 12, 19))
        self.assertEquals(5200, self.cashflow.series["amount"].sum())

    def testExportToCsv(self):
        self.cashflow.generate_series('Salary', 1000)
        with TempDirectory() as tmp:
            self.cashflow.export_to_csv(tmp.path, 'cash_flow_estimate.csv')
            file_contents = tmp.read('cash_flow_estimate.csv', 'utf-8').splitlines()
        self.assertEquals(len(file_contents), len(self.cashflow.series) + 1) #File contains headers

    def testExportToPng(self):
        self.cashflow.generate_series('Salary', 1000)
        with TempDirectory() as tmp:
            self.cashflow.export_to_png(tmp.path, 'cash_flow_estimate.png')
            tmp.compare(expected=['cash_flow_estimate.png'])
