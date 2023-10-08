import json
import pandas as pd

datajson=json.loads(open('json/gamedata/zh_CN/gamedata/excel/uniequip_table.json').read())

maxparam3List=0
maxparamList=0

for key in datajson["missionList"].keys():
    if len(datajson["missionList"][key]["paramList"]) > maxparamList:
        maxparamList = len(datajson["missionList"][key]["paramList"])
    if len(datajson["missionList"][key]["paramList"]) > 3:
        if len(datajson["missionList"][key]["paramList"][3].split(";")[0].split(","))>maxparam3List:
            maxparam3List=len(datajson["missionList"][key]["paramList"][3].split(";")[0].split(","))

Module = []
Moduletemplate = []
Moduledesc=[]
ModuleparamList =[[] for x in range(maxparamList)]
Moduleparam4List=[[] for x in range(maxparam3List)]

for key in datajson["missionList"].keys():
    Module.append(key)
    Moduletemplate.append(datajson["missionList"][key]["template"])
    Moduledesc.append(datajson["missionList"][key]["desc"])
    for x in range(maxparamList):
        if (x<len(datajson["missionList"][key]["paramList"])):
            ModuleparamList[x].append(datajson["missionList"][key]["paramList"][x])
        else:
            ModuleparamList[x].append("")
    for y in range(maxparam3List):
        if len(datajson["missionList"][key]["paramList"]) > 3:
            if(y<len(datajson["missionList"][key]["paramList"][3].split(";")[0].split(","))):
                Moduleparam4List[y].append(datajson["missionList"][key]["paramList"][3].split(";")[0].split(",")[y])
            else:
                Moduleparam4List[y].append("")
        else:
            Moduleparam4List[y].append("")

dfList=[Module,Moduletemplate,Moduledesc]
dfindex=['Module','template','Desc']

for i in range(maxparamList):
    dfList.append(ModuleparamList[i])
    dfindex.append("para"+str(i))
    
for i in range(maxparam3List):
    dfList.append(Moduleparam4List[i])
    dfindex.append("para3."+str(i))

df=pd.DataFrame(dfList,index=dfindex).transpose()

'''with pd.ExcelWriter('excel/Pytest.xlsx') as writer:
    df.to_excel(writer, sheet_name='test', index=False)'''

df.to_csv('excel/Pytest.csv',sep='|', index=False)

line = 'sep=|' 
with open('excel/Pytest.csv', 'r+') as file: 
    file_data = file.read() 
    file.seek(0, 0) 
    file.write(line  +'\n'+ file_data)

print("\nDataframe Completed !!!")