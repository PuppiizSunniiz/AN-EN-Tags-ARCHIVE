import json

#########################################################################################################
# JSON
#########################################################################################################
json_char   =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/character_table.json").read())
json_mod    =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/uniequip_table.json").read())
json_range  =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/range_table.json").read())

#########################################################################################################
# Function
#########################################################################################################
def msgbox(self) -> str:
    if isinstance(self,str):
        repeat=len(self)+8
        return "#"*repeat+"\n#   "+self+"   #\n"+"#"*repeat
    elif isinstance(self,list):
        repeat=max(map(lambda x: len(x),self))+15
        return "#"*repeat+("\n#    ").join(self)+"\n"+"#"*repeat

def Continue() -> bool:
    print(msgbox("Continue ? (Y/N)"))
    con=input()
    match con.lower():
        case "n":
            return False
        case "y":
            return True
        case default:
            Continue()

def Charname(self) -> str:
    '''
        Get self as Char key
        Check if appellation in Russian
        Return as Eng name
        
        # Russian = {'Гум': 'Gummy', 'Зима': 'Zima', 'Истина': 'Istina', 'Позёмка': 'Pozëmka', 'Роса': 'Rosa'}
        
        return NameCheck(json_char[self]["appellation"])
    '''
    def NameCheck(self):
        Russian = {'Гум': 'Gummy', 'Зима': 'Zima', 'Истина': 'Istina', 'Позёмка': 'Pozëmka', 'Роса': 'Rosa'}
        if self in Russian.keys():
            return Russian[self]
        else:
            return self
        
    return NameCheck(json_char[self]["appellation"])

def Charcheck():
    def Charout(text,mode):
        print(msgbox("What "+text+" to check ?"))
        charin=input()
        
        chars=[]
        for key in DB["Char"][mode].keys():
            if charin.lower() in key.lower():
                chars.append([key,DB["Char"][mode][key]])
        if len(chars):
            print("Result :")
            for x in range(len(chars)):
                print(chars[x])
            print("Search result :",len(chars))
        else:
            print(f"No Char Code with \"{charin}\" exist")
        
    print(msgbox(["\n#  Select Mode",
          "1 : Char Name from Char Code",
          "2 : Char Code from Char Name",
          "0 : Exit"
          ]))
    char=input()
    match char:
        case "0":
            return False
        case "1":
            Charout("Char Code","Code2Name")
        case "2":
            Charout("Char Name","Name2Code")
        case default:
            Charcheck()
        
    return Continue()

def Modcheck():
    print(msgbox("What Module Num to check ? (1/2/3 or 0 : Exit)" ))
    modnum=int(input())
    
    if modnum =="0":
        return False
    elif modnum not in [1,2,3]:
        Modcheck()
    
    mod=[]
    for key in json_mod["charEquip"].keys():
        if len(json_mod["charEquip"][key])>modnum:
            mod.append(Charname(key)+" "+key)
    sorted(mod)
    mod.append("Search result :"+str(len(mod)))
    print("\n".join(mod))
    return Continue()

def Rangecheck():
    print(msgbox("What Range to check ? (S: Show All Range | 0 : Exit)" ))
    rangeid=input()
    
    if rangeid == "0":
        return False
    elif rangeid.lower() == "s":
        print(list(DB["Range"].keys()))
        Rangecheck()
    elif rangeid.lower() not in DB["Range"].keys():
        print(rangeid,"is not Range ID")
        Rangecheck()
    else :
        for row in range(len(DB["Range"][rangeid])):
            print("".join(DB["Range"][rangeid][row]))
    
    return Continue()

'''
    def Tagcheck():
        print(msgbox("What Tag(s) to check ? (up to 5 tags | 0 : Exit)"))
        tags=input()
    
        if tags=="0":
            return False
        else :
            tagscheck(tags)
    
        def tagscheck(tags):
            tags = tags.split(" ")
            for i in range(len(tags)):
                match tags[i]:
                    case "Guard"
                        
                    case "dps"
                        tags[i] = DPS
                
        
'''
#########################################################################################################
# Ready
#########################################################################################################
DB={}

CharReady={"Code2Name":{},"Name2Code":{}}
OpsExclude=[] # "isNotObtainable": true
for key in json_char.keys():
    if "char_" in key:
        CharReady["Code2Name"][key]=Charname(key)
        CharReady["Name2Code"][Charname(key)]=key
        if json_char[key]["isNotObtainable"]:
            OpsExclude.append(key)
DB["Char"]=CharReady

RangeReady={} # 🟥🟧🟨🟩🟦🟪🟫⬛⬜🔳
for rangeid in json_range.keys():
    temp =[]
    for grid in json_range[rangeid]["grids"]:
        temp.append([grid["col"],grid["row"]])
    
    maxX=max([x[0] for x in temp])
    minX=min([x[0] for x in temp]+[0])
    maxY=max([y[1] for y in temp])
    minY=min([y[1] for y in temp]+[0])
    
    rangearray=[["⬛" for x in range(maxX-minX+1)] for y in range(maxY-minY+1)]
    
    rangearray[maxY][abs(min(0,minX))]="🔳"
    tryx=""
    tryy=[]
    for userange in temp:
        if userange == [0,0]:
            rangearray[userange[1]+maxY][userange[0]+abs(min(0,minX))]="🟨"
        else:
            rangearray[userange[1]+maxY][userange[0]+abs(min(0,minX))]="🟦"
    rangearray.append(str(temp))
    RangeReady[rangeid]=rangearray
DB["Range"]=RangeReady

jsonout=json.dumps(DB,indent=4, ensure_ascii=False)
with open('py/dict.json','w') as JSON:
    JSON.write(jsonout)

TagReady={}

'''json_gacha  =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/gacha_table.json").read())
json_gachaEN  =   json.loads(open("json/gamedata/en_US/gamedata/excel/gacha_table.json").read())
gachapon={}
for tag in json_gacha["gachaTags"]:
    gachapon[tag["tagId"]]={"tagName":tag["tagName"]}
for tag in json_gachaEN["gachaTags"]:
    gachapon[tag["tagId"]].update({"EN":tag["tagName"]})
gacha=json.dumps(gachapon,indent=4, ensure_ascii=False)
with open('temp/tag.json','w') as JSON:
    JSON.write(gacha)'''

#########################################################################################################
# Go !!!
#########################################################################################################
while(True):
    #repeat=49
    Boolcheck=True
    text=["\n#  Select Function",
          "1 : Char Name/Code Check",
          "M : Mod Check",
          "R : Range Check",
          "0 : Exit"
          ]
    print(msgbox(text))
    exe=input()
    match exe.lower():
        case "0":
            break
        case "1":
            while(Boolcheck):
                Boolcheck=Charcheck()
        case "m":
            while(Boolcheck):
                Boolcheck=Modcheck()
        case "r":
            while(Boolcheck):
                Boolcheck=Rangecheck()
        case default:
            pass