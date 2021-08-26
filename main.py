# Code Info : This project is designed to take two files of the same extention and find the differences and add those differences into another csv file

from typing import Text
import PySimpleGUI as sg
import re, time
from PySimpleGUI.PySimpleGUI import Column, RELIEF_RIDGE, Tree, Window
from openpyxl.workbook.workbook import Workbook
import pandas as pd
import numpy as np
import openpyxl
supportedextensions = {'csv','xlsx','xlsm','json'}

#build Window 1
layoutprefile = [
    [sg.Text('Select the two files you wish to use')],
    [sg.Text('File 1'), sg.InputText(),sg.FileBrowse()],
    [sg.Text('File 2'), sg.InputText(),sg.FileBrowse()],
    [sg.Submit('Next'), sg.Cancel('Exit')]
]
window1 = sg.Window('University of North Florida CSV Comparison Tool', layoutprefile)
while True:
    event, values = window1.read()
    # end if exit is clicked
    if event in (None, 'Exit', 'Cancel'):
        secondwindow = 0
        break
    elif event == 'Next':
        #now we check if two same file types have been selected 
        file1temp = file2temp = pass_stage = next_stage = None
        file1, file2 = values[0],values[1]
        if file1 and file2:
            file1temp = re.findall('.+:\/.+.', file1)
            file2temp = re.findall('.+:\/.+.', file1)
            pass_stage = 1

            #check if the paths for both files is valid 
            if not file1temp and file1temp is not None:
                print('Error :File 1 path is not valid')
                pass_stage = 0
            elif not file2temp and file2temp is not None:
                print('Error :File 2 path is not valid')
                pass_stage = 0
            
            #check if file extensions are the same
            elif re.findall('/.+?/.+\.(.+)', file1) != re.findall('/.+?/.+\.(.+)', file2):
                print('Error : Files have different extensions')
                pass_stage = 0

            #check if extension is supported
            elif re.findall('/.+?/.+\.(.+)', file1)[0] not in supportedextensions or re.findall('/.+?/.+\.(.+)', file1)[0] not in supportedextensions:
                print('Error : File extention not supported at this time')
                pass_stage = 0

            #checks if files are the same
            elif file1 == file2:
                print('Error : Files are the same, please select a different one')
                pass_stage = 0

            #now lets read the files
            elif pass_stage == 1:
                print('First stage passed : Accessing files now')
                try: 
                    if re.findall('/.+?/.+\.(.+)', file1)[0] == 'csv':
                        df1, df2 = pd.read_csv(file1), pd.read_csv(file2)
                    elif re.findall('/.+?/.+\.(.+)', file1)[0] == 'json':
                        df1, df2 = pd.read_json(file1), pd.read_json(file2)
                    elif re.findall('/.+?/.+\.(.+)', file1)[0] in ['xlsx', 'xlsm']:
                        df1, df2 = pd.read_excel(file1), pd.read_excel(file2) 
                    proceedtofindcommonkeys = 1
                except IOError:
                    print('Error : File not accessible')
                    proceedtofindcommonkeys = 0
                except UnicodeDecodeError:
                    print("Error : File includes a unicode character that cannot be decoded with the default UTF decryption")
                    proceedtofindcommonkeys = 0
                except Exception as e:
                    print('Error : ', e)
                    proceedtofindcommonkeys = 0
        else:
            print('Error : Please choose 2 files')
        if proceedtofindcommonkeys == 1 :
            window1.close()
            secondwindow = 1
            break

#########################################################################This section completed#################################################################
if secondwindow != 1:
    exit()

#######Compare Column by Column Code work ############
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# Finding the matched rows 
df = df1.merge(df2, how = 'inner' ,indicator=False)
       
# Finding unique rows in file 1
unique_df1 = df1.merge(df2, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']

# Finding unique rows in file 2
unique_df2 = df1.merge(df2, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='right_only']

##################################################

#### Compare all selected headers code work #################
for i in range(len(df1.columns.values)):
    keys1 = "key_one"+str(i)
# for o in range(len(df2.columns.values)):
#     keys2 = "key_two"+str(o)
#Second UI
layoutpostfile = [
    [sg.Text('Location of file one'), sg.InputText(file1,disabled = True, size = (75,2))],
    [sg.Text('Location of file two'), sg.InputText(file2,disabled = True, size = (75,2))],
    [sg.Text('Comparison 1')],
    [sg.Text('Please choose one header for each comparison from file one')],
    [sg.Radio(df1.columns.values[i],"test1", default = False, key =keys1[i])for i in range(len(df1.columns.values))],
    [sg.Text('Please choose one header for each comparison from file two')],
    [sg.Radio(df2.columns.values[i],"test2", default = False,)for i in range(len(df2.columns.values))],
    [sg.Button("Add Another Comparison")],
    [sg.Button("Compare all selected headers")],
    [sg.Button('Compare column to column'), sg.Cancel('Exit')] 
]

      
window2 = sg.Window('File Compare', layoutpostfile)      
datakeydefined = 0
definedkey = []
while True:  # The Event Loop
    event, values = window2.read()
    if event in (None, 'Exit', 'Cancel'):
        break
    elif event == 'Choose another batch':
        window2.close()
    elif event == 'Compare all selected headers':
        print(len(keys1))
    #     for key in keys1:
    #         if key.get()==True:
    #             print(window2.FindElement(key).get())
    elif event == 'Compare column to column':
        xlwriter = pd.ExcelWriter('files/column_to_column.xlsx')
        df.to_excel(xlwriter, sheet_name= 'all matched rows', index = False , header=True)
        unique_df1.to_excel(xlwriter, sheet_name = 'unique_rows_file1', index = False, header = True)
        unique_df2.to_excel(xlwriter, sheet_name = 'unique_rows_file2', index = False, header = True)
        xlwriter.close()
        sg.popup('Request Completed, please check files folder')

        

    