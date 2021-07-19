import PySimpleGUI as sg
import re, time
import datacompy
import pandas as pd
supportedextensions = {'csv','xlsx','xlsm','json'}

#build Window 1
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
            keylist1 = [] #list of headers from file 1
            keylist2 = [] #list of headers from file 2
            keylist =[] #list of similar headers in both files
            formslist = [] #List of headers to be displayed in UI

            # Now lets add headers to their list 
            for header in df1.columns:
                if header not in keylist1:
                    keylist1.append(header)
            for header in df2.columns:
                if header not in keylist2:
                    keylist2.append(header)
            for item in keylist1:
                if item in keylist2:
                    keylist.append(item)
            if len(keylist) == 0:
                print('No similar headers')
                Window2 = 0
            else:
                window1.close()
                window2 = 1
                break




                


            
        

