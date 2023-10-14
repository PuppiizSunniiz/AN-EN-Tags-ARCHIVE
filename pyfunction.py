def CharReady(JSON,mode=0):
    '''
        Get character_table -> Return Code2Name Name2Code dict
        
        Mode 1 : ["Code2Name"]
        Mode 2 : ["Name2Code"]
        Mode 3 : ["Exclude"]
        Default : All
    '''
    def Charname(JSON,key) -> str:
        def NameCheck(appellation):
            Russian = {'Гум': 'Gummy', 'Зима': 'Zima', 'Истина': 'Istina', 'Позёмка': 'Pozëmka', 'Роса': 'Rosa'}
            if appellation in Russian.keys():
                return Russian[appellation]
            else:
                return appellation
            
        return NameCheck(JSON[key]["appellation"])

    Chars={"Code2Name":{},"Name2Code":{}}
    OpsExclude=[] # "isNotObtainable": true
    for key in JSON.keys():
        Chars["Code2Name"][key]=Charname(JSON,key)
        Chars["Name2Code"][Charname(JSON,key)]=key
        if JSON[key]["isNotObtainable"] and "char_" in key:
            OpsExclude.append([key,Charname(JSON,key)])
    Chars["Exclude"]=OpsExclude
    match mode :
        case 1 :
            return Chars["Code2Name"]
        case 2 :
            return Chars["Name2Code"]
        case 3 :
            return Chars["Exclude"]
        case _ :
            return Chars