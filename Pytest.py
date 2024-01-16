import json

buildEN=json.loads(open("json/gamedata/en_US/gamedata/excel/building_data.json").read())
RIIC=json.loads(open("json/ace/riic.json").read())

for buff in buildEN["buffs"].keys():
    RIIC[buff]["descformat"]=buildEN["buffs"][buff]["description"]

dumpling=json.dumps(RIIC,indent=4, ensure_ascii=False)
with open("json/ace/riic.json",'w') as JSON :
    JSON.write(dumpling)