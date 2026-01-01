"""
-------------------------------------------------------------------------------
Subprime Auto Machine Learning
Formatting ABS-EE Files
-------------------------------------------------------------------------------
@author: wcarpenter
@date:   Jan 2026

Organizing ABS-EE auto loan files into usable formats.

Default format is to create single loan observations from a panel series.
The reporting files could also be used to create a panel for additional 
analysis.
-------------------------------------------------------------------------------
"""

# Process
# get file / deal path
# compile all files together
# label each unique loan in order
# identify the last observations (most recent, paydown, default, charge-off)
# add in user-defined variables - DLQ history, depreciation

import os
import pandas as pd

PATH    = r'C:/Users/William/OneDrive/Desktop/Auto/' 
FOLDERS = ['Santander Drive 2023-1']

col_map  = pd.read_excel(PATH + 'abs_ee_col_mapping.xlsx')
col_dict = dict(zip(col_map['abs_ee_col'], col_map['col_name'])) 

for folder in FOLDERS:
    print("Parsing:", folder)
    full_path = PATH + folder
    file_list = []
    counter = 0
    # Generating master file
    for f in os.listdir(full_path):
        if 'csv' in f.lower():
            # First file creates master
            if counter == 0:
                lm = pd.read_csv(full_path + '/' + f, header=0)
                counter += 1
            # Appending files to master
            else:
                print('Appending:', f)
                obs = pd.read_csv(full_path + '/' + f, header=0)
                lm = pd.concat([lm, obs])
    # Data cleaning
    # Column renaming
    lm = lm.rename(columns=col_dict)
    # Adjustments
    lm['deal'] = folder
    
    date_cols = ['begin_date', 'end_date', 'orig_date', 'loan_maturity_date',
                 'first_pay_date', 'interest_paid_thru', 'zero_bal_date',
                 'servicing_transfer_date', 'demand_resolution_date']
    
    lm[date_cols] = lm[date_cols].apply(pd.to_datetime, errors='coerce')
    
    lm = lm.sort_values(['asset_num', 'begin_date'], ascending=[True, True])
    
    # exp = lm.tail(5000)
    # Added variables
    # ever 30+ DLQ
    # ever 60+ DLQ
    # ever 90+ DLQ
    # 90+ DLQ past 12mo
    # 30+ DLQ past 3mo
 











