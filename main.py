# Code Info : This project is designed to take two files of the same extention and find the differences and add those differences into another csv file

from tkinter.constants import DISABLED, FALSE
import PySimpleGUI as sg
import re, time
from PySimpleGUI.PySimpleGUI import RELIEF_RIDGE, Window
import datacompy
import pandas as pd
import numpy as np
supportedextensions = {'csv','xlsx','xlsm','json'}

#build Window 1
layoutprefile = [
    [sg.Text('Select the two files you wish to use')],
    [sg.Text('File 1'), sg.InputText(),sg.FileBrowse()],
    [sg.Text('File 2'), sg.InputText(),sg.FileBrowse()],
    #---List One---#
    #[sg.Output(size=(61,5))],
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
                temp_pass = 0
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
            first_file_headers = [] #list of headers from file 1
            second_file_headers = [] #list of headers from file 2
            similar_headers =[] #list of similar headers in both files
            display1 = [] #List of headers to be displayed in UI for first file
            display2= [] #list of headers to be displayed in UI for second file

#########################################################################This section completed##################################################################
            # Now lets add headers to their list 
            for header in df1.columns:
                if header not in first_file_headers:
                    first_file_headers.append(header)
            for header in df2.columns:
                if header not in second_file_headers:
                    second_file_headers.append(header)
            for item in first_file_headers:
                if item in second_file_headers:
                    similar_headers.append(item)
            window1.close()
            secondwindow = 1
            break
# First UI completed and we found the similar headers from both files

if secondwindow != 1:
    exit()

maxlen = 0
maxlen1 = 0
for header in first_file_headers:
    if len(str(header)) > maxlen:
        maxlen = len(str(header))
if maxlen > 25:
    maxlen = 25
elif maxlen < 10:
    maxlen = 15    

for header in second_file_headers:
    if len(str(header)) > maxlen1:
        maxlen1 = len(str(header))
if maxlen1 > 25:
    maxlen1 = 25
elif maxlen1 < 10:
    maxlen1 = 15    

#we need to split the keys to four columns for first file
for index,item in enumerate(first_file_headers):
    if index == 0: i =0
    if len(first_file_headers) >= 4 and i == 0:
        display1.append([sg.Checkbox(first_file_headers[i], size=(maxlen,None)),sg.Checkbox(first_file_headers[i+1], size=(maxlen,None)),sg.Checkbox(first_file_headers[i+2], size=(maxlen,None)),sg.Checkbox(first_file_headers[i+3], size=(maxlen,None))])
        i += 4
    elif len(first_file_headers) > i:
        if len(first_file_headers) - i - 4>= 0:
            display1.append([sg.Checkbox(first_file_headers[i], size=(maxlen,None)),sg.Checkbox(first_file_headers[i+1], size=(maxlen,None)),sg.Checkbox(first_file_headers[i+2], size=(maxlen,None)),sg.Checkbox(first_file_headers[i+3], size=(maxlen,None))])
            i += 4
        elif len(first_file_headers) - i - 3>= 0:
            display1.append([sg.Checkbox(first_file_headers[i], size=(maxlen,None)),sg.Checkbox(first_file_headers[i+1], size=(maxlen,None)),sg.Checkbox(first_file_headers[i+2], size=(maxlen,None))])
            i += 3
        elif len(first_file_headers)- i - 2>= 0:
            display1.append([sg.Checkbox(first_file_headers[i], size=(maxlen,None)),sg.Checkbox(first_file_headers[i+1], size=(maxlen,None))])
            i += 2
        elif len(first_file_headers) - i - 1>= 0:
            display1.append([sg.Checkbox(first_file_headers[i], size=(maxlen,None))])
            i += 1
        else:
            sg.Popup('Error: Uh-oh, something\'s gone wrong!')      

#we need to split the keys to four columns for second file
for index,item in enumerate(second_file_headers):
    if index == 0: i =0
    if len(second_file_headers) >= 4 and i == 0:
        display2.append([sg.Checkbox(second_file_headers[i], size=(maxlen,None)),sg.Checkbox(second_file_headers[i+1], size=(maxlen,None)),sg.Checkbox(second_file_headers[i+2], size=(maxlen,None)),sg.Checkbox(second_file_headers[i+3], size=(maxlen,None))])
        i += 4
    elif len(second_file_headers) > i:
        if len(second_file_headers) - i - 4>= 0:
            display2.append([sg.Checkbox(second_file_headers[i], size=(maxlen,None)),sg.Checkbox(second_file_headers[i+1], size=(maxlen,None)),sg.Checkbox(second_file_headers[i+2], size=(maxlen,None)),sg.Checkbox(second_file_headers[i+3], size=(maxlen,None))])
            i += 4
        elif len(second_file_headers) - i - 3>= 0:
            display2.append([sg.Checkbox(second_file_headers[i], size=(maxlen,None)),sg.Checkbox(second_file_headers[i+1], size=(maxlen,None)),sg.Checkbox(second_file_headers[i+2], size=(maxlen,None))])
            i += 3
        elif len(second_file_headers)- i - 2>= 0:
            display2.append([sg.Checkbox(second_file_headers[i], size=(maxlen,None)),sg.Checkbox(second_file_headers[i+1], size=(maxlen,None))])
            i += 2
        elif len(second_file_headers) - i - 1>= 0:
            display2.append([sg.Checkbox(second_file_headers[i], size=(maxlen,None))])
            i += 1
        else:
            sg.Popup('Error: Uh-oh, something\'s gone wrong!')            

#Second UI
layoutpostfile = [
    [sg.Text('Location of file one'), sg.InputText(file1,disabled = True, size = (75,2))],
    [sg.Text('Location of file two'), sg.InputText(file2,disabled = True, size = (75,2))],
    [sg.Text('Comparison 1')],
    [sg.Text('Please choose one header for each comparison from file one')],
    [sg.Frame(layout=[*display1],title ='Please select one for comparison', relief = sg.RELIEF_RIDGE)],
    [sg.Text('Please choose one header for each comparison from file two')],
    [sg.Frame(layout=[*display2],title ='Please select one for comparison', relief = sg.RELIEF_RIDGE)],
    [sg.Button("Add Another Comparison")],
    [sg.Button("Compare all selected headers")],
    [sg.Button('Compare column to column'), sg.Cancel('Exit')]
    
]

#######Compare Column by Column Code work ############
dffile1 = pd.read_excel(file1)
dffile2 = pd.read_excel(file2)
comparevalues = dffile1.values == dffile2.values

rows,cols = np.where(comparevalues == False)

for item in zip(rows,cols):
    dffile1.iloc[item[0],item[1]] = '{} --> {}'.format(dffile1.iloc[item[0], item[1]], dffile2.iloc[item[0], item[1]])
       
##################################################

#### Compare all selected headers code work #################

       
window2 = sg.Window('File Compare', layoutpostfile).Finalize()       
datakeydefined = 0
definedkey = []
while True:  # The Event Loop
    event, values = window2.read()
    if event in (None, 'Exit', 'Cancel'):
        break
    elif event == 'Choose another batch':
        window2.close()


    elif event == 'Compare column to column':
        dffile1.to_excel('files/output.xlsx', index = False , header=True)
        

    