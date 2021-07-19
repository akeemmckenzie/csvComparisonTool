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
    # elif event == 'Proceed':
        

