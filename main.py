# Code Info : This project is designed to take two files of the same extention and find the differences and add those differences into another csv file

from genericpath import isdir
from tkinter.constants import TRUE
from typing import Text
import PySimpleGUI as sg
import re, time
from PySimpleGUI.PySimpleGUI import Button, Column, RELIEF_RIDGE, Element, InputText, Tree, Window
from numpy import inner
from openpyxl.workbook.workbook import Workbook
import pandas as pd
import openpyxl
import os
import copy
supportedextensions = {'csv','xlsx','xlsm','json'}


#build Window 1
layoutprefile = [
    [sg.Text('Select the two files you wish to use')],
    [sg.Text('File 1'), sg.InputText(),sg.FileBrowse()],
    [sg.Text('File 2'), sg.InputText(),sg.FileBrowse()],
    [sg.Submit('Next'), sg.Cancel('Exit')],
]
window1 = sg.Window('University of North Florida CSV Comparison Tool', layoutprefile,)
while True:
    event, values = window1.read()
    if event in (None, 'Exit', 'Cancel'):
        secondwindow = 0
        break
    if event == 'Exit':
        break
    elif event == 'Next':
        #now we check if two same file types have been selected 
        file1temp = file2temp = pass_stage = next_stage = None
        file1, file2 = values[0],values[1]
        proceedtofindcommonkeys = 0
        if file1 and file2:
            file1temp = re.findall('.+:\/.+.', file1)
            file2temp = re.findall('.+:\/.+.', file1)
            pass_stage = 1

            #check if the paths for both files is valid 
            if not file1temp and file1temp is not None:
                sg.popup('Error :File 1 path is not valid')
                pass_stage = 0
            elif not file2temp and file2temp is not None:
                sg.popup('Error :File 2 path is not valid')
                pass_stage = 0
            
            #check if file extensions are the same
            elif re.findall('/.+?/.+\.(.+)', file1) != re.findall('/.+?/.+\.(.+)', file2):
                sg.popup('Error : Files have different extensions')
                pass_stage = 0

            #check if extension is supported
            elif re.findall('/.+?/.+\.(.+)', file1)[0] not in supportedextensions or re.findall('/.+?/.+\.(.+)', file1)[0] not in supportedextensions:
                sg.popup('Error : File extention not supported at this time')
                pass_stage = 0

            #checks if files are the same
            elif file1 == file2:
                sg.popup('Error : Files are the same, please select a different one')
                pass_stage = 0

            #now lets read the files
            elif pass_stage == 1:
                try: 
                    if re.findall('/.+?/.+\.(.+)', file1)[0] == 'csv':
                        df1, df2 = pd.read_csv(file1), pd.read_csv(file2)
                    elif re.findall('/.+?/.+\.(.+)', file1)[0] == 'json':
                        df1, df2 = pd.read_json(file1), pd.read_json(file2)
                    elif re.findall('/.+?/.+\.(.+)', file1)[0] in ['xlsx', 'xlsm']:
                        df1, df2 = pd.read_excel(file1), pd.read_excel(file2) 
                    proceedtofindcommonkeys = 1
                except IOError:
                    sg.popup('Error : File not accessible')
                    proceedtofindcommonkeys = 0
                except UnicodeDecodeError:
                    sg.popup('Error : File includes a unicode character that cannot be decoded with the default UTF decryption')
                    proceedtofindcommonkeys = 0
                except Exception as e:
                    sg.popup('Please select two compatible files with atleast two similar headers')
                    proceedtofindcommonkeys = 0
        else:
            sg.popup('Please select two compatible files with atleast two similar headers')
        if proceedtofindcommonkeys == 1 :
            window1.hide()
            secondwindow = 1
            break
#########################################################################This section completed#################################################################
if secondwindow != 1:
    exit()

#######Compare Column by Column Code work ############

#Read file given (Files accessible are csv,xlsx and json)
if re.findall('/.+?/.+\.(.+)', file1)[0] == 'csv':
    df1, df2 = pd.read_csv(file1), pd.read_csv(file2)
elif re.findall('/.+?/.+\.(.+)', file1)[0] == 'json':
    df1, df2 = pd.read_json(file1), pd.read_json(file2)
elif re.findall('/.+?/.+\.(.+)', file1)[0] in ['xlsx', 'xlsm']:
    df1, df2 = pd.read_excel(file1), pd.read_excel(file2)

#Convert Columns to string
df1 = df1.astype(str)
df2 = df2.astype(str)


##################################################

#### Compare all selected headers code work #################
keys1 = []
for k in range(len(df1.columns.values)):
    keys1.append(df1.columns.values[k]+'_file1')
keys2 = []
for p in range(len(df2.columns.values)):
    keys2.append(df2.columns.values[p]+ '_file2')

file1_val_selected = []
file2_val_selected = [] 

# Function to convert  
def listToString(s): 
    
    # initialize an empty string
    str1 = "," 
    
    # return string  
    return (str1.join(s))

#Create location for output
m = re.search('/Users/(.+?)/', file1)
if m:
    username = m.group(1)
    path = '/Users/'+username+'/Documents/csvcomparison'
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
        print("The new directory is created")
    else :
        print("directory already exists")


layoutpostfile = [
    [sg.Text('Location of file one'), sg.InputText(file1,disabled = True, size = (75,2))],
    [sg.Text('Location of file two'), sg.InputText(file2,disabled = True, size = (75,2))],
    [sg.Text('Output Location default'), sg.InputText(path),sg.FolderBrowse()],
    [sg.Text('Comparison')],
    [sg.Text('Please choose one header for each comparison from File one')],
    [sg.Radio(df1.columns.values[i],"test1", default = False, key= keys1[i])for i in range(len(df1.columns.values))],
    [sg.Text('Please choose one header for each comparison from File two')],
    [sg.Radio(df2.columns.values[i],"test2", default = False, key = keys2[i])for i in range(len(df2.columns.values))],
    [sg.Button('Add Comparison'), sg.Button('Clear Comparison')],
    [sg.InputText('File 1 :' + listToString(file1_val_selected), readonly= True ,key = 'text1', size = (100,150))],
    [sg.InputText('File 2 :' + listToString(file2_val_selected), readonly= True ,key = 'text2', size = (100,150))],
    [sg.Button("Compare"), sg.Button('Select different files')] 
]

      
window2 = sg.Window('File Compare', layoutpostfile)     
while True:  # The Event Loop
    event, values = window2.read()
    if event in (None, 'Exit', 'Cancel'):
        break

    elif event == 'Add Comparison':
        for i in range(len(keys1)):
            if(values[keys1[i]]== TRUE):
                file1_val_selected.append(window2.Element(keys1[i]).Key.removesuffix('_file1'))
                window2.Element(keys1[i]).update(value= False)
                window2['text1'].update('File 1:' +listToString(file1_val_selected))
        for i in range(len(keys2)):
            if(values[keys2[i]]== TRUE):
                file2_val_selected.append(window2.Element(keys2[i]).Key.removesuffix('_file2'))
                window2.Element(keys2[i]).update(value= False)
                window2['text2'].update('File 2:' +listToString(file2_val_selected))

    elif event == 'Clear Comparison':
        file1_val_selected.clear()
        file2_val_selected.clear()
        window2['text1'].update('File 1:' +listToString(file1_val_selected))
        window2['text2'].update('File 2:' +listToString(file2_val_selected))


    elif event == 'Compare':
        for i in range(len(keys1)):
            if(values[keys1[i]]== TRUE):
                file1_val_selected.append(window2.Element(keys1[i]).Key.removesuffix('_file1'))
                window2['text1'].update('File 1:' +listToString(file1_val_selected))
        for i in range(len(keys2)):
            if(values[keys2[i]]== TRUE):
                file2_val_selected.append(window2.Element(keys2[i]).Key.removesuffix('_file2'))
                window2['text2'].update('File 2:' +listToString(file2_val_selected))
        
        # Finding the matched rows 
        sf = df1.merge(df2, how ='inner', left_on= file1_val_selected, right_on= file2_val_selected, indicator=False)
        # Finding unique rows in file 1
        unique_sf1 = df1.merge(df2, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
        # Finding unique rows in file 2
        unique_sf2 = df1.merge(df2, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='right_only']

        xlwriter = pd.ExcelWriter(path +'/compare_selected.xlsx')
        sf.to_excel(xlwriter, sheet_name= 'all matched rows', index = False , header=True)
        unique_sf1.to_excel(xlwriter, sheet_name = 'unique_rows_file1', index = False, header = True)
        unique_sf2.to_excel(xlwriter, sheet_name = 'unique_rows_file2', index = False, header = True)
        xlwriter.close()
        if sg.PopupYesNo('Request Completed, Continue to open file?') == "YES":
            os.system('start "excel" "C:\"' + path +'/compare_selected.xlsx')
        file1_val_selected.clear()
        file2_val_selected.clear()
        window2['text1'].update('File 1:' +listToString(file1_val_selected))
        window2['text2'].update('File 2:' +listToString(file2_val_selected))

    elif event == 'Select different files':
        window2.hide()
        window1.un_hide()
        window1.refresh()
        

    # elif event == 'Compare column to column':
    #     xlwriter = pd.ExcelWriter(path + '/column_to_column.xlsx')
    #     df.to_excel(xlwriter, sheet_name= 'all matched rows', index = False , header=True)
    #     unique_df1.to_excel(xlwriter, sheet_name = 'unique_rows_file1', index = False, header = True)
    #     unique_df2.to_excel(xlwriter, sheet_name = 'unique_rows_file2', index = False, header = True)
    #     xlwriter.close()
        # if sg.('Request Completed, Continue to open file?') == 'OK':
        #     os.system('start "excel" "C:\"'+ path + '/column_to_column.xlsx')


    
        
        
    