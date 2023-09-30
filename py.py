import json

json_char=json.loads(open("json/gamedata/zh_CN/gamedata/excel/character_table.json").read())

def msgbox(self):
    if isinstance(self,str):
        repeat=len(self)+8
        return "#"*repeat+"\n#   "+self+"   #\n"+"#"*repeat
    elif isinstance(self,list):
        repeat=max(map(lambda x: len(x),self))+15
        return "#"*repeat+("\n#    ").join(self)+"\n"+"#"*repeat

def Continue():
    print(msgbox("Continue ? (Y/N)"))
    exe=input()
    match exe.lower():
        case "n":
            return False
        case "y":
            return True
        case default:
            Continue()

def NameCheck(self):
    Russian = {'Гум': 'Gummy', 'Зима': 'Zima', 'Истина': 'Istina', 'Позёмка': 'Pozëmka', 'Роса': 'Rosa'}
    if self in Russian.keys():
        return Russian[self]
    else:
        return self

def Char():
    print(msgbox("What Char Code to check ?"))
    char=input()

    chars=[]
    for key in json_char.keys():
        if char in key and "char" in key:
            chars.append([key,NameCheck(json_char[key]["appellation"])])
            
    if len(chars):
        print("Result")
        for x in range(len(chars)):
            print(chars[x])
    else:
        print(f"No Char Code with \"{char}\" exist")
    return Continue()

while(True):
    repeat=49
    Boolcheck=True
    text=["\n#  Select Function",
          "1 : get Char Name from Char Code",
          "0 : Exit"
          ]
    print(msgbox(text))
    exe=input()
    match exe:
        case "0":
            break
        case "1":
            while(Boolcheck):
                Boolcheck=Char()
        case default:
            pass