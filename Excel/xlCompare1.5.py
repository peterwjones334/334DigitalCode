""""
Title: Compare Spreadsheet Script
Description: This script compare indices in columns in 2 spreadsheet and identifies differences.
Author: 334 Digital 
Date: 2024-05-17
Version: 1.5

Dependencies:
    - pandas
    - datetime
    - logging
    - pathlib


Usage:
    xlCompare1.5.py

License:
    MIT License

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
import os
import time
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path

# Define global variables for column names
COLUMNS = ['Index', 'Item', 'Description']
SHEETS = ['Sheet1', 'Differences', 'Additions', 'Removals']
# Define indices for key and comparison columns
KEY_COLUMN_INDEX = 0  # 'Index'
COMPARISON_COLUMN_INDICES = [1, 2]  # ['Item', 'Description']
MAX_ATTEMPTS = 5
DELAY_BETWEEN_ATTEMPTS = 2

class SpreadsheetComparator:
    """SpreadsheetComparator is designed to handle operations related to comparing Excel sheets, detecting index differences, additions, and removals between two sheets"""

    def __init__(self, folderpath):
        self.folderpath = folderpath

    def compare(self, truth_file, distr_file, output_file):
        """Loads sheets, compares them, and writes the results to an output Excel file."""
        self.check_and_create_file(truth_file)  # Ensure truth_file exists or create it
        try:
            sheet1 = self.load_sheet(truth_file, SHEETS[0])
            sheet2 = self.load_sheet(distr_file, SHEETS[0])
            differences, additions, removals = self.compare_sheets(sheet1, sheet2)
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                differences.to_excel(writer, index=False, sheet_name=SHEETS[1])
                additions.to_excel(writer, index=False, sheet_name=SHEETS[2])
                removals.to_excel(writer, index=False, sheet_name=SHEETS[3])  # Assuming SHEETS[3] is the removals sheet
        except Exception as e:
            logging.error(f"Failed to compare sheets: {e}")   
    
    def safe_open_excel_writer(self, path, engine='openpyxl', max_attempts=MAX_ATTEMPTS, delay_between_attempts=DELAY_BETWEEN_ATTEMPTS):
        """Attempt to open an ExcelWriter object with retries on PermissionError."""
        attempt = 0
        while attempt < max_attempts:
            try:
                return pd.ExcelWriter(path, engine=engine)
            except PermissionError:
                logging.error(f"Attempt {attempt + 1}: Unable to write to {path}. The file may be open. Please close the file.")
                time.sleep(delay_between_attempts)
                attempt += 1
        raise PermissionError(f"Failed to write to {path} after {max_attempts} attempts.")

    def create_spreadsheet(self, filename):
        """Creates a template spreadsheet with predefined data."""
        df = pd.DataFrame(columns=COLUMNS)
        data = [
            {COLUMNS[0]: 1, COLUMNS[1]: 'Item1', COLUMNS[2]: 'Description of Item1'},
            {COLUMNS[0]: 2, COLUMNS[1]: 'Item2', COLUMNS[2]: 'Description of Item2'},
            {COLUMNS[0]: 3, COLUMNS[1]: 'Item3', COLUMNS[2]: 'Description of Item3'}
        ]
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
        try:
            with self.safe_open_excel_writer(filename) as writer:
                df.to_excel(writer, index=False, sheet_name=SHEETS[0])
        except PermissionError as e:
            logging.error(e)

    def load_sheet(self, file_path, sheet_name):
        """Loads a sheet from the specified Excel file."""
        try:
            return pd.read_excel(file_path, sheet_name=sheet_name)
        except FileNotFoundError:
            raise FileNotFoundError("The file was not found.")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
    
    def check_and_create_file(self, file_path):
        """Check if the file exists, and create it if it does not."""
        if not os.path.exists(file_path):
            self.create_spreadsheet(file_path)    

    def compare_sheets(self, sheet1, sheet2):
        """Compares two sheets based on a key and other comparison columns, identifying differences and additions."""
        key_column = COLUMNS[KEY_COLUMN_INDEX]
        comparison_columns = [COLUMNS[i] for i in COMPARISON_COLUMN_INDICES]

        necessary_columns = [key_column] + comparison_columns
        sheet1_prepared = sheet1.loc[:, necessary_columns].copy()
        sheet2_prepared = sheet2.loc[:, necessary_columns].copy()

        merged = pd.merge(sheet1_prepared, sheet2_prepared, on=key_column, how='outer', suffixes=('_left', '_right'), indicator=True)
        differences = pd.DataFrame()
        for col in comparison_columns:
            diff_mask = (merged[f'{col}_left'] != merged[f'{col}_right']) & (merged['_merge'] == 'both')
            col_diff = merged[diff_mask]
            differences = pd.concat([differences, col_diff], ignore_index=True)
        additions = merged[merged['_merge'] == 'right_only']
        removals_mask = merged['_merge'] == 'left_only'
        removal = merged[removals_mask][key_column]
        removals = sheet1_prepared.loc[sheet1_prepared[key_column].isin(removal)]
        return differences, additions, removals

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    
    # Define the base folder path
    folderpath = Path('D:/process/project52')

    # Define file paths
    truth_file = folderpath / 'truth.xlsx'
    distr_file = folderpath / 'distribution.xlsx'
    today = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    output_file = folderpath / f'comparison_results_{today}.xlsx'
    
    # Initialize and run spreadsheet comparison
    comparator = SpreadsheetComparator(folderpath)
    comparator.compare(truth_file, distr_file, output_file)
