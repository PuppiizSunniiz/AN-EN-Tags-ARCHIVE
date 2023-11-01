import json

###
# json
###

jsonlist = json.loads(open("json/gamedata/zh_CN/gamedata/excel/activity_table.json").read())

formulas = jsonlist["activity"]["TYPE_ACT29SIDE"]["act29side"]["formDataMap"]

notes = jsonlist["activity"]["TYPE_ACT29SIDE"]["act29side"]["fragDataMap"]

parse = {}
for note in notes.keys():
    parse[note]=notes[note]["fragName"]

mood={"乐":"Happy","怒":"Fury","哀":"Sorrow","惧":"Fear"}

color={"乐":"🟨","怒":"🟥","哀":"🟦","惧":"🟩"}

for i in formulas.keys():
    #print(formulas[i]["formDesc"],[parse[x] for x in formulas[i]["fragIdList"]])
    #print([mood[parse[x]] for x in formulas[i]["fragIdList"]])
    print(formulas[i]["formDesc"],[parse[x] for x in formulas[i]["fragIdList"]],"".join([color[parse[x]] for x in formulas[i]["fragIdList"]]))
    