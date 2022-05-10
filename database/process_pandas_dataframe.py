import pandas as pd
import re
import numpy as np


def find_start(df):
    """
    given an unprocessed dataframe, find the start of the trades, which
    can be located at "schedule b: transaction". We then return the df_index,
    and the row that it starts on.

    :df: list of pandas dataframes
    :return: the number of df, know as df_index, and the row in that specific df
    """
    for i in range(len(df)):
        index = df[i].index[df[i].iloc[:, 0].str.lower() == "schedule b: transactions"].tolist()
        if index:
            return i, index[0]


def get_column_for_regex(df, df_index, regex, start_row=0):
    """
    Given a list of pandas dataframe, the index of which dataframe to start with
    a regex expression, and an optional start row, we search until we find a
    column and row value that gives a match to the given regex expression.

    :df: list of pandas dataframe
    :df_index: int, the index of the df to start at
    :regex: regex string, the regex expression to match on
    :start_row: int, optional, if not indicated starts at zero.
    """
    number_of_columns = len(df[df_index].columns)
    number_of_rows = len(df[df_index])
    column_number = 1
    row_number = start_row
    regex_result = re.match(regex, str(df[df_index].iloc[row_number, column_number]))
    while regex_result is None and column_number < number_of_columns:
        if row_number < (number_of_rows - 1):
            # print(row_number, column_number)
            row_number += 1
        elif column_number < (number_of_columns - 1):
            # print(row_number, column_number)
            row_number = start_row
            column_number += 1
        else:
            break

        regex_result = re.match(regex, str(df[df_index].iloc[row_number, column_number]))

    if regex_result is None:
        print(f"exception raised here: {df_index}, {row_number}, {column_number}")
        raise Exception("Column not found for given regex")

    return column_number


def generate_entry(df, df_index, row, regex_result, new_db_page):
    """
    this is an extremely complicated function that basically files in all the
    data for a single trade. It mostly works of matching regex expressions and
    taking the information from there

    :df: list of pandas dataframes
    :df_index: int, the starting index of which panda dataframe to start
    :row: int, the row to start at
    :regex_result: regex matching result, look at process dataframe for more info
    :new_db_page: Bool, deals with the fact that the pandas dataframes look
    different depending on if the transaction b: started on this page or if
    it started on a different page
    :return: returns a dict with all the information in it
    """
    description_regex = r"^description: (.+)$"
    stock_regex = r"^\s*(?!description:|location:)\s*(.*)\s*\((?!one|two)([\w | .]{1,5})\).*$"
    bounds_regex = r"^[a-zA-Z]*\s*\$?(?!\d{1,4}\/)([\d]+,?[\d]+)\s*-?\s*\$?([\d]*,?\d*).*$"
    time_regex = r"^[a-zA-z]*\s*(\d{1,2}\/\d{1,2}\/\d{2,4})\s*$"
    transaction_type_regex = r"\s*([SPsp])\s*$"

    row_shift_flag = False
    df_index_shift_flag = False
    prev_row = row
    prev_df_index = df_index

    company_name = regex_result[1].strip()
    ticker = regex_result[2].upper()
    if new_db_page:
        column_time = get_column_for_regex(df, df_index, time_regex)
    else:
        column_time = get_column_for_regex(df, df_index, time_regex, row)

    time_regex_result = re.match(time_regex, str(df[df_index].iloc[row, column_time]))

    while time_regex_result is None:
        if row == 0:
            df_index -= 1
            row = len(df[df_index]) - 1
            column_time = get_column_for_regex(df, df_index, time_regex, row - 1)
        else:
            row -= 1
        time_regex_result = re.match(time_regex, str(df[df_index].iloc[row, column_time]))
    # print(df_index, row)

    # print(df_index, row, column_time)
    owner_date = pd.to_datetime(time_regex_result[1])

    if new_db_page:
        transaction_bounds = get_column_for_regex(df, df_index, transaction_type_regex)
    else:
        transaction_bounds = get_column_for_regex(df, df_index, transaction_type_regex, row)

    transaction_type = df[df_index].iloc[row, transaction_bounds]

    if new_db_page:
        column_bounds = get_column_for_regex(df, df_index, bounds_regex)
    else:
        column_bounds = get_column_for_regex(df, df_index, bounds_regex, row)
    bounds_regex_result = re.match(bounds_regex, df[df_index].iloc[row, column_bounds])

    # print(df[df_index].iloc[row, column_bounds])
    lower_bound = bounds_regex_result[1]
    upper_bound = ''

    if bounds_regex_result[2] == '':
        if row == len(df[df_index]) - 1:
            upper_bound = lower_bound
        else:
            regex_result = re.match(bounds_regex, str(df[df_index].iloc[row + 1, column_bounds]))
            # print(df_index, row, column_bounds)
            if regex_result is None:
                upper_bound = lower_bound
            else:
                upper_bound = regex_result[1]

    else:
        upper_bound = bounds_regex_result[2]

    row = prev_row
    df_index = prev_df_index

    description = None

    location_regex = r"^location: (.+)$"

    row += 1
    max_row_not_hit = True
    if row >= len(df[df_index]) - 1:
        max_row_not_hit = False
    else:
        line_info = str(df[df_index].iloc[row, 0]).lower()
        location_regex_result = re.match(location_regex, line_info)

    while max_row_not_hit and (line_info == 'nan' or location_regex_result is not None):
        if len(df[df_index]) - 1 == row:
            max_row_not_hit = False
        else:
            row += 1
            line_info = str(df[df_index].iloc[row, 0]).lower()
            location_regex_result = re.match(location_regex, line_info)

    if max_row_not_hit:
        description_regex_result = re.match(description_regex, line_info)
        if description_regex_result is not None:
            description = description_regex_result[1]

    return {'Member Name': np.nan,
            'Member District': np.nan,
            'Company': company_name,
            'Ticker': ticker,
            'Type': transaction_type,
            'Date': owner_date,
            'Value Lower Bound': lower_bound,
            'Value Upper Bound': upper_bound,
            'Description': description,
            'Link': np.nan}, row


def process_dataframe(df, pdf_path):
    """
    Given an unprocessed list of pandas dataframes and a path to the pdf, generates
    a new pandas dataframe with all the data about the trades filled in. This
    pandas dataframe is in the exact same shape as our final SQL database.

    :df: list of pandas dataframes
    :pdf_path: string, path to the pdf where df was created from
    :return: a pandas dataframe with all of the trade data from the given df/pdf
    """
    pdf_db = pd.DataFrame(columns=['Member Name', 'Member District', 'Company', 'Ticker', 'Type', 'Date',
                                   'Value Lower Bound', 'Value Upper Bound', 'Description', 'Link'])

    # description_regex = r"^description: (.+)$"
    stock_regex = r"^\s*(?!description:|location:)\s*(.*)\s*\((?!one|two)([\w | .]{1,5})\).*$"
    # bounds_regex = r"^[a-zA-Z]*\s*\$?([\d,]+)\s*-?\s*\$?([\d,]*).*$"
    honorifics_regex = r"^(hon.?|mr.?|miss|mrs.?|ms.?|dr.?|professor.?|gen.?|)\s*(.+)$"
    link_regex = r"^(\d{4})[\w_/\s\.]*_(\d+\.pdf)$"
    root_link = "https://disclosures-clerk.house.gov/public_disc/financial-pdfs"

    new_db_page = False

    name_regex_result = re.match(honorifics_regex, df[0].iloc[0, 1].lower())
    name = name_regex_result[2].strip()
    link_regex_result = re.match(link_regex, pdf_path.lower().strip())
    link = root_link + "/" + link_regex_result[1] + "/" + link_regex_result[2]

    district = df[0].iloc[2, 1]
    find_start_result = find_start(df)
    if find_start_result is None:
        return pdf_db

    df_index, row = find_start_result

    # row += 1
    stock_info = str(df[df_index].iloc[row, 0]).lower()

    while stock_info != "schedule c: earned income" and stock_info != "schedule d: liabilities":
        regex_result = re.match(stock_regex, stock_info)
        if regex_result is not None:
            result_dict, new_row = generate_entry(df, df_index, row, regex_result, new_db_page)
            result_dict['Member Name'] = name
            result_dict['Member District'] = district
            result_dict['Link'] = link
            pdf_db = pd.concat([pdf_db, pd.Series(result_dict).to_frame().T], ignore_index=True)

        if len(df[df_index].index) - 1 == row:
            row = 0
            df_index += 1
            print("HELLO")
            new_db_page = True
        else:
            row += 1
        # print(stock_info)
        stock_info = str(df[df_index].iloc[row, 0]).lower()

    return pdf_db

