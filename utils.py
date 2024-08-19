import csv
import pandas as pd
from pathlib import Path
import numpy as np
dat = Path("/Users/11nho/Developer/MedPC/!2019-07-29")

def read_file(
    file #Accepts Text or CSV Files
    ):
    #TODO implement txt of csv file handling
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        csvContents=list(reader)
    csvContents = [x for x in csvContents if x != []]
    return csvContents

def parse_file(
    fileContents #File data converted to list of lists
    ):
    metadata = ['Start Date','End Date','Subject','Experiment','Group','Box','Start Time','End Time','MSN']
    experimentSep = [x for x,row in enumerate(fileContents) if row[0].split(':')[0] == metadata[0]]
    experimentSep.append(-1)
    print(experimentSep)

    for i,exp in enumerate(experimentSep):
        if exp == -1:
            continue
        else:
            start = exp
            stop = experimentSep[i+1]
            session = fileContents[start:stop]
            sessionInfo = [row for row in session if row[0].split(':')[0] in metadata]
            sessionInfoList = [x for y in sessionInfo for x in y]
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
                        out = cleanStr.split(' ')[1:-1]
                        for dataPoint in out:
                            dataOut[key].append(int(dataPoint).round().astype('Int64'))
            dataOut['Metadata'] = sessionInfoList
            df = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in dataOut.items()]))
            columnToMove = df.pop('Metadata')
            df.insert(0, 'Metadata', columnToMove)
def save_data(
    dataframe, #Takes in a dataframe
    savefiletype
    ):
    #TODO handle different potential save operations (csv,xlsx,pkl)
    #TODO also eliminate outputting extra column on indexes        
    # Given a dict of dataframes, for example:
    # dfs = {'gadgets': df_gadgets, 'widgets': df_widgets}
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    for sheetname, df in dfs.items():  # loop through `dict` of dataframes
        df.to_excel(writer, sheet_name=sheetname)  # send df to writer
        worksheet = writer.sheets[sheetname]  # pull worksheet object
        for idx, col in enumerate(df):  # loop through all columns
            series = df[col]
            max_len = max((
                series.astype(str).map(len).max(),  # len of largest item
                len(str(series.name))  # len of column name/header
                )) + 1  # adding a little extra space
            worksheet.set_column(idx, idx, max_len)  # set column width
    writer.save()