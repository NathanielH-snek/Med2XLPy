import csv
import pandas as pd
from pathlib import Path
import numpy as np
import re

dat = Path("/Users/11nho/Developer/MedPC/!2019-07-29")

def readFile(
    file #Accepts Text or CSV Files
    ):
    #TODO implement txt of csv file handling
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        csvContents=list(reader)
    csvContents = [x for x in csvContents if x != []]
    return csvContents

def parseFile(
    fileContents #File data converted to list of lists
    ):
    metadata = ['Start Date','End Date','Subject','Experiment','Group','Box','Start Time','End Time','MSN']
    experimentSep = [x for x,row in enumerate(fileContents) if row[0].split(':')[0] == metadata[0]]
    experimentSep.append(-1)

    dfDict = {}
        
    for i,exp in enumerate(experimentSep):
        if exp == -1:
            continue
        else:
            start = exp
            stop = experimentSep[i+1]
            session = fileContents[start:stop]
            sessionInfo = [row for row in session if row[0].split(':')[0] in metadata]
            sessionInfoList = [x for y in sessionInfo for x in y]
            metaDict = {x.split(':')[0].strip(): x.split(':')[1].replace(" ", "") for x in sessionInfoList}
            lastInfo = session.index(sessionInfo[-1])
            dataOnly = session[(lastInfo + 1):-1]
            dataVarLocs = [x for x,row in enumerate(dataOnly) if row[0].split(':')[0].isalpha()]
            dataVars = [dataOnly[x][0].split(':')[0] for x in dataVarLocs]
            dataVarLocs.append(-1)
            dataOut = {key: [] for key in dataVars}
            for j,val in enumerate(dataVarLocs):
                if val == dataVarLocs[-1]:
                    continue
                else:
                    begin = val
                    end = dataVarLocs[j+1]
                    varData = dataOnly[begin:end]
                    key = varData[0][0].split(':')[0]
                    del varData[0]
                    for row in varData:
                        cleanStr = ' '.join(row[0].split())
                        out = cleanStr.split(' ')[1:]
                        for dataPoint in out:
                            dataOut[key].append(round(int(float(dataPoint))))
            dataOut['Metadata'] = sessionInfoList
            df = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in dataOut.items()]))
            columnToMove = df.pop('Metadata')
            df.insert(0, 'Metadata', columnToMove)
            filename = f"{metaDict['Subject']}_{metaDict['Start Date']}_{metaDict['MSN']}"
            dfDict[filename] = df
    return dfDict
            
def saveData(
    dataframes: dict, #Takes in a dictionary of dataframes
    #savefiletype,
    folderpath
    ):
    
    #TODO handle different potential save operations (csv,xlsx,pkl)
    #TODO also eliminate outputting extra column on indexes        
    # Given a dict of dataframes, for example:
    # dfs = {'gadgets': df_gadgets, 'widgets': df_widgets}
    for sheetname, df in dataframes.items():  # loop through `dict` of dataframes
        savename = re.sub(r'[^\w_. -]', '_', sheetname)
        savelocation = Path(f"{folderpath}/{savename}.xlsx")
        print(savelocation)
        writer = pd.ExcelWriter(savelocation, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1',index=False)  # send df to writer
        worksheet = writer.sheets['Sheet1']  # pull worksheet object
        for i, col in enumerate(df.columns):
            width = max(df[col].apply(lambda x: len(str(x))).max(), len(col))
            worksheet.set_column(i, i, width)
        writer.close()