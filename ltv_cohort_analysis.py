#!/usr/bin/env python3

import pandas as pd
import numpy as np
import xlrd
import datetime
import sys

if len(sys.argv) < 2:
	print("Use program by entering: name_of_excel_file time_period")
	sys.exit()

file_name = str(sys.argv[1]) + ".xlsx"
time_period = str(sys.argv[2])

#Creates the initial data frame
print("Reading excel file and creating dataframe...")

df = pd.read_excel(file_name, sheet_name='raw_data')
df.columns = ['transaction_id', 'customer_id', 'date', 'v']
df['event_period'] = pd.DatetimeIndex(df['date']).to_period(time_period)
cg = df[['customer_id', 'date']].groupby(['customer_id']).min()
cg['cohort'] = pd.DatetimeIndex(cg['date']).to_period(time_period)
cg = cg['cohort']
df = df.join(cg, on='customer_id')

# Creates pivot table and drops into Excel with cohort/customer_id
print("Organizing complete customer purchase history...")
pivot_for_excel = pd.pivot_table(df, values='v', index=['customer_id', 'cohort'], columns=['event_period'], aggfunc=np.sum).sort_index(level=1)

# Creates a new dataframe with each cohort's size
print("Calculating cohort sizes...")
cgcount = df.copy()
cgcount.set_index('cohort', inplace=True)
cgcount = cgcount.groupby(cgcount.index)['customer_id'].apply(lambda x: x.nunique())

# Generates the date range in the period we need since the first cohort started
min_date = df['date'].min()
dates = pd.period_range(start=min_date, end=datetime.datetime.now(), freq=time_period)
date_series = pd.Series(range(1, len(dates)+1))

#Lines up month 1 for each cohort, with cohort the name of the index and event_period the name of the columns
print("Justifying purchases by cohort period...")

cohort_month = []
for i in range(len(dates)):
	x = list(range(1, len(dates)+1))
	cohort_month.append(x)

t = pd.DataFrame(data=cohort_month, index=dates, columns=dates).transpose()

shift_start = 0
for column in t:
	t[column] = t[column].shift(shift_start)
	shift_start += 1

t = t.transpose()
t = t.stack()

# Justifies cohort_period as index
print("Organizing purchases by cohort period into pivot table...")

pivot_for_calc = pd.pivot_table(df, values='v', index=['cohort'], columns=['event_period'], aggfunc=np.sum).transpose().unstack()
result = pd.concat([pivot_for_calc, t], axis=1)
result = result.reset_index()
result.columns = ['cohort', 'event', 'agg', 'period_range']
result = result.drop(['event'], axis=1).pivot_table(values='agg', index='period_range', columns='cohort').cumsum().divide(cgcount, axis=1)


# Calculates the weighted average
print("Calculating weighted average...")

wacgcount = cgcount.copy().sort_index(ascending=False)

weighted_average = []
for i in range(len(cgcount)):
	x = (result.iloc[i] * wacgcount[i:]).sum() / wacgcount[i:].sum()
	weighted_average.append(x)

w_a = pd.DataFrame(weighted_average)
w_a.index = w_a.index + 1
w_a.columns = ['weighted_average']

#Drops everything into an Excel Doc
print("Creating Excel Doc...")

excel_output = str(sys.argv[1]) + "_output.xlsx"

cgcount = cgcount.to_frame()

writer = pd.ExcelWriter(excel_output)
pivot_for_excel.to_excel(writer,'Customer Purchase Hist')
cgcount.to_excel(writer,'Cohort Sizes')
w_a.to_excel(writer, 'Weighted Average')
result.to_excel(writer, 'Cohorts by Period')
writer.save()

#Make sure you have only four columns in the spreadsheet
#Don't add .xlsx to the end of your file_name in the command line
#Delete any future orders (will fix this for the future)
#