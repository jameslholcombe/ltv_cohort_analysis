# ltv_cohort_analysis
This program uses the `pandas` library to calculate the weighted average value of a customer lifetime. The program takes a raw transaction history in Excel (`.xlsx`) and returns an Excel file with tabs:
- Complete customer transaction history
- Cohort size
- Weighted average customer value
- Aggregated cohort value

## Preparing the data

Before running the program, save an Excel file that has columns, in this order: `transaction_id`, `customer_id`, `transaction_date`, `value`. The `value` column can be any potential aggregated value. Common use cases would be: a dollar amount (eg. gross revenue, gross margin), a count (eg. number of items bought so the integer 1, 2, 5, etc), an integer of time value (eg. seconds, minutes, hours).
Name the tab the data is in `raw_data`.

The names of the columns don't matter, but you **DO** need headers, and the columns should be in the correct order.

## To run the program:
1. Install `virtualenv` on your system:
  - On OSX or Linux, this will probably work: `$ sudo pip install virtualenv`
  - On Ubuntu Linux, this will probably work: `$ sudo apt-get install python-virtualenv`
2. Create a new directory 
  - `$ cd new_directory`
  - `$ virtualenv venv`
3. Activate the corresponding virtual environment
- `$ . venv/bin/activate`
4. Install dependencies
- `pip install pandas`
- `pip install xlrd`
5. The program will take two command line arguments: name of file without the `.xlsx` file type and the period you would like to run the cohort analysis on. Here are the common period options for a cohort analysis:
  - `M` : Month
  - `D` : Day
  - `H` : Hour

## Examples of running the program

`$ python3 ltv_cohort_analysis.py my_excel_transaction_file M`

`$ python3 ltv_cohort_analysis.py sql_dump D`
