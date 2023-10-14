import pandas
import json
from pyfunction import CharReady

#########################################################################################################
# JSON
#########################################################################################################
json_building       =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/building_data.json").read())

json_char           =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/character_table.json").read())
json_charEN         =   json.loads(open("json/gamedata/en_US/gamedata/excel/character_table.json").read())

json_handbook       =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/handbook_info_table.json").read())
json_mod_battle     =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/battle_equip_table.json").read())
json_mod_table      =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/uniequip_table.json").read())
json_stage          =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/stage_table.json").read())

json_item           =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/item_table.json").read())
'''json_itemEN        =   json.loads(open("json/gamedata/en_US/gamedata/excel/item_table.json").read())
json_itemJP        =   json.loads(open("json/gamedata/ja_JP/gamedata/excel/item_table.json").read())
json_itemKR        =   json.loads(open("json/gamedata/ko_KR/gamedata/excel/item_table.json").read())'''

json_akmaterial     =   json.loads(open("json/akmaterial.json").read())
json_trait          =   json.loads(open("json/tl-attacktype.json").read())
#########################################################################################################
# test
#########################################################################################################
'''
    # gender
    for key in json_handbook["handbookDict"].keys():  
        if key.split("_")[0]=="char":
            print(key,json_handbook["handbookDict"][key]["storyTextAudio"][0]["stories"][0]["storyText"].split("\n")[1].split("】")[1])
    # class
    for key in json_char.keys():
    Class.append(json_char[key]["profession"])
'''

#########################################################################################################
# Prep
#########################################################################################################
newchars = ["Verdant","Vendela","Delphine", "Hoederer"]
newmods = [["Horn",1],["Ashlock",1],["Firewhistle",1],["Delphine",1],["Verdant",1],["Fiammetta",2],["Ebenholz",3]]
newmats = ["31074","31073","31084","31083"]
newtrait ={}
akhrOutput = []

CharReady=CharReady(json_char)

Classparse= {'SNIPER':"狙击", 'PIONEER':"先锋", 'TANK':"重装",  'MEDIC':"医疗", 'SUPPORT':"辅助", 'SPECIAL':"特种", 'WARRIOR':"近卫",  'CASTER':"术师"}

#########################################################################################################
# Chars
#########################################################################################################
'''    
    Char :
    json/tl-akhr.json
        - add new >>> char id / name / camp (???) / type (class) / level (rarity) / sex / tag (Rarity+Range/Melee+op tag) / hidden (recruit)
        ** need json
            + char table - 
            + char story - 
'''
for newchar in newchars:
    newcode=CharReady["Name2Code"][newchar]
    akhrOutput.append({
                            "id": newcode,
                            "name_cn": json_char[newcode]["name"],
                            "name_en": newchar,
                            "name_jp": "",
                            "name_kr": "",
                            "characteristic_cn": "",
                            "characteristic_en": "",
                            "characteristic_jp": "",
                            "characteristic_kr": "",
                            "camp": "",
                            "type": Classparse[json_char[newcode]["profession"]],
                            "level": int(json_char[newcode]["rarity"][-1]),
                            "sex": json_handbook["handbookDict"][newcode]["storyTextAudio"][0]["stories"][0]["storyText"].split("\n")[1].split("】")[1],
                            "tags": ["高级资深干员" for x in range(1) if json_char[newcode]["rarity"][-1]=="6"]+ \
                                    ["资深干员" for x in range(1) if json_char[newcode]["rarity"][-1]=="5"]+ \
                                    ["新手" for x in range(1) if json_char[newcode]["rarity"][-1]=="2"]+ \
                                    ["近战位" for x in range(1) if json_char[newcode]["position"]=="MELEE"]+ \
                                    ["远程位" for x in range(1) if json_char[newcode]["position"]=="RANGED"]+ \
                                    json_char[newcode]["tagList"],
                            "hidden": True,
                            "globalHidden": True
    })
    newtrait[json_char[newcode]["description"]]={"name":newchar,
                                                 "code":newcode,
                                                 "mode":"newchars"}

dumpling=json.dumps(akhrOutput,indent=4, ensure_ascii=False)
with open("update/tl-akhr.json",'w') as JSON :
    JSON.write(dumpling)
    
#########################################################################################################
# Mats
#########################################################################################################

'''
    Item :
        # akmatuses.html
            - add new botton for new mat >>> 'Name' / 'item id'
            ** need json
                + item
        # json/akmaterial.json
            - List new >>> mat name / pic id / rarity / drop list / workshop recipe
            ** need json
                + item (+ all server for item name)
                + stage
        # json/tl-item.json
            - List new >>> mat id / name
            ** need json
                + item (+ all server for item name)
'''

#akmatuses.html
matbotton=[]
for mat in newmats:
    matbotton.append("<button type=\"button\" onclick=\"clickBtnTag(this)\" class=\"btn btn-sm btn-secondary ak-btn btn-tag my-1 button-tag\" data-toggle=\"tooltip\" data-placement=\"top\" title=\""+json_item["items"][mat]["name"]+"\" mat-id=\""+mat+"\"></button>")

matbotton.sort(reverse=False,key=lambda mat : mat.split("\"")[-2][0:-1]) #sort mat id
matbotton.sort(reverse=True,key=lambda mat : mat.split("\"")[-2][-1]) #sort rarity

with open("update/akmatuses.txt",'w') as writer:
    writer.write("\n\n".join(matbotton))

#json/akmaterial.json
akmat=[]
Dropparse={"ALWAYS":"Always","ALMOST":"Common","USUAL":"Medium","OFTEN":"Rare","SOMETIMES":"Very Rare"}
for i in range(len(newmats)):
    mat=newmats[i]
    matsource={}
    for stage in json_item["items"][mat]["stageDropList"]:
        matsource[json_stage["stages"][stage["stageId"]]["code"]]=Dropparse[stage["occPer"]]
    matcraft={}
    for recipe in json_building["workshopFormulas"].keys():
        if json_building["workshopFormulas"][recipe]["itemId"]==mat:
            for cost in json_building["workshopFormulas"][recipe]["costs"]:
                matcraft[json_item["items"][cost["id"]]["name"]]=cost["count"]
    akmat.append({
                    "id": len(json_akmaterial)+i,
                    "itemId": mat,
                    "IconID": json_item["items"][mat]["iconId"],
                    "name_cn": json_item["items"][mat]["name"],
                    "name_en": "",
                    "name_jp": "",
                    "name_kr": "",
                    "name_tw": "",
                    "level": int(json_item["items"][mat]["rarity"][-1]),
                    "source": matsource,
                    "madeof": matcraft
    })
    
dumpling=json.dumps(akmat,indent=4, ensure_ascii=False)
with open("update/akmaterial.json",'w') as JSON :
    JSON.write(dumpling)

#json/tl-item.json
tlmat=[]
for mat in newmats:
    tlmat.append({
                    "itemId":  mat,
                    "name_cn": json_item["items"][mat]["name"],
                    "name_en": "",
                    "name_jp": "",
                    "name_kr": "",
                    "name_tw": ""
    })

dumpling=json.dumps(tlmat,indent=4, ensure_ascii=False)
with open("update/tl-item.json",'w') as JSON :
    JSON.write(dumpling)
    
#########################################################################################################
# Mats
#########################################################################################################   
'''
    Mod :
        # json/TempModuletalentsTL.json
            - add new mod name and Talent(+pot) description TL for new mod in CN 
            ** BY HAND only
            ** need json
                + mod table - for char list
                + mod battle - for mod talent desc and blackboard
'''

modtl={}
for charlist in newmods:
    char=CharReady["Name2Code"][charlist[0]]
    modcode=json_mod_table["charEquip"][char][charlist[1]]
    if json_mod_battle[modcode]["phases"][0]["parts"][0]["overrideTraitDataBundle"]["candidates"][0]["additionalDescription"]:
        newtrait[json_mod_battle[modcode]["phases"][0]["parts"][0]["overrideTraitDataBundle"]["candidates"][0]["additionalDescription"]]={"name":charlist[0],
                                                    "code":modcode,
                                                    "mode":"newmods"}
    else :
        newtrait[json_mod_battle[modcode]["phases"][0]["parts"][0]["overrideTraitDataBundle"]["candidates"][0]["overrideDescripton"]]={"name":charlist[0],
                                                    "code":modcode,
                                                    "mode":"newmods"}
    tempphase=[]
    for phase in [1,2]:
        for part in json_mod_battle[modcode]["phases"][phase]["parts"]:
            temppart=[]
            if part["target"] in ["TALENT_DATA_ONLY","TALENT"] and not part["isToken"] and part["addOrOverrideTalentDataBundle"]["candidates"][0]["upgradeDescription"]!="":
                for pot in range(len(part["addOrOverrideTalentDataBundle"]["candidates"])):
                    candidate = part["addOrOverrideTalentDataBundle"]["candidates"][pot]
                    if char in json_charEN and candidate["talentIndex"]!=-1:
                        temppart.append({
                                "name":json_charEN[char]["talents"][candidate["talentIndex"]]["candidates"][pot-len(part["addOrOverrideTalentDataBundle"]["candidates"])]["name"],
                                "EN":json_charEN[char]["talents"][candidate["talentIndex"]]["candidates"][pot-len(part["addOrOverrideTalentDataBundle"]["candidates"])]["description"],
                                "CN":json_char[char]["talents"][candidate["talentIndex"]]["candidates"][pot-len(part["addOrOverrideTalentDataBundle"]["candidates"])]["description"],
                                "mod":candidate["upgradeDescription"],
                                "upgradeDescription":""
                        })
                    else:
                        temppart.append({
                                "name":candidate["name"],
                                "CN":json_char[char]["talents"][candidate["talentIndex"]]["candidates"][pot-len(part["addOrOverrideTalentDataBundle"]["candidates"])]["description"],
                                "mod":candidate["upgradeDescription"],
                                "upgradeDescription":""
                        })
        tempphase.append(temppart)
    modtl[modcode]=tempphase

dumpling=json.dumps(modtl,indent=4, ensure_ascii=False)
with open("update/TempModuletalentsTL.json",'w') as JSON :
    JSON.write(dumpling)

#########################################################################################################
# Trait
#########################################################################################################
'''
    Char + Mod :
        # json/tl-attacktype.json
            - add new char / mod triat that not already exist
            ** nedd json
                + char table - for char trait
                + mod battle - for mod trait
                + <itself> - for recheck exist
        
'''
pop=[]
for key in newtrait.keys():
    if key in json_trait["full"].keys():
        pop.append(key)
for key in pop:
    newtrait.pop(key)

dumpling=json.dumps(newtrait,indent=4, ensure_ascii=False)
with open("update/tl-attacktype.json",'w') as JSON :
    JSON.write(dumpling)

print("Update Completed")