import PySimpleGUI as sg
import re, time
import datacompy
import pandas as pd
supportedextensions = {'csv','xlsx','xlsm','json'}

layoutprefile = [
    [sg.Text('Select the two files you wish to use')],
    [sg.Text('File 1'), sg.InputText(),sg.FileBrowse()],
    [sg.Text('File 2'), sg.InputText(),sg.FileBrowse()],
    #---List One
    [sg.Output(size=(61,5))],
    [sg.Submit('Proceed'), sg.Cancel('Exit')]
]
window1 = sg.Window('University of North Florida CSV Comparison Tool', layoutprefile)
while True:
    event, values = window1.read()
    # end if exit is clicked
    if event in (None, 'Exit', 'Cancel'):
        Window2 = 0
        break
    elif event == 'Proceed':
        #now we check if two same file types have been selected 
        file1temp = file2temp = temp_pass = next_stage = None
        file1, file2 = values[0],values[1]
        if file1 and file2:
            file1temp = re.findall('.+:\/.+.', file1)
            file2temp = re.findall('.+:\/.+.', file1)
            temp_pass = 1
            if not file1temp and file1temp is not None:
                print('Error :File 1 path is not valid')
                temp_pass = 0
            elif not file2temp and file2temp is not None:
                print('Error :File 2 path is not valid')
                temp_pass = 0

            
        

