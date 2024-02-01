import json

#########################################################################################################
# JSON
#########################################################################################################
SandboxCN=json.loads(open("json/gamedata/zh_CN/gamedata/excel/sandbox_table.json").read())
SandboxEN=json.loads(open("json/gamedata/en_US/gamedata/excel/sandbox_table.json").read())

#########################################################################################################
# Prep
#########################################################################################################
FoodDict ={"Food":{},"Foodmat":{}}
BuildDict={}
WeatherDict = {}

ItemData= SandboxEN["itemDatas"]

#########################################################################################################
# Food
#########################################################################################################
FoodProduct = SandboxEN["sandboxActTables"]["act1sandbox"]["foodProduceDatas"]
FoodmatProduct = SandboxEN["sandboxActTables"]["act1sandbox"]["foodmatDatas"]
FoodStamina=SandboxEN["sandboxActTables"]["act1sandbox"]["foodStaminaDatas"]

for foodID in FoodProduct.keys():
    FoodDict["Food"][foodID]={
                        "Name" : ItemData[foodID]["itemName"],
                        "Recipe" : [ x for x in FoodProduct[foodID]["mainMaterialItems"]],
                        "Buff" : ItemData[foodID]["itemUsage"],
                        "BuffDetail" : [x["blackboard"][0] for x in SandboxEN["sandboxActTables"]["act1sandbox"]["runeDatas"][foodID]["runes"]],
                        "Energy" : FoodStamina[foodID]["potCnt"],
                        "Stamina" : FoodStamina[foodID]["foodStaminaCnt"]
                    }
    
for foodmatID in FoodmatProduct.keys():
    FoodDict["Foodmat"][foodmatID]={
                        "Name" : ItemData[foodmatID]["itemName"],
                        "Buff" : FoodmatProduct[foodmatID]["buffDesc"],
                        "Buff2" : ItemData[foodmatID]["itemUsage"],
                        "BuffDetail" : SandboxEN["sandboxActTables"]["act1sandbox"]["runeDatas"][FoodmatProduct[foodmatID]["buffId"]]["runes"][0]["blackboard"] if FoodmatProduct[foodmatID]["buffId"] else None,
                        "Energy" : FoodStamina[foodmatID]["potCnt"],
                        "Stamina" : FoodStamina[foodmatID]["foodStaminaCnt"]
                    }

#########################################################################################################
# Building
#########################################################################################################
BuildProduce = SandboxEN["sandboxActTables"]["act1sandbox"]["buildProduceDatas"]
BuildUnlock = SandboxEN["sandboxActTables"]["act1sandbox"]["buildProduceUnlockDatas"]

for buildID in BuildProduce.keys():
    BuildDict[buildID]={
                            "Name" : ItemData[buildID]["itemName"],
                            "Type": BuildProduce[buildID]["itemTypeText"],
                            "Recipe" : [ x for x in  BuildProduce[buildID]["materialItems"]],
                            "Effect": BuildUnlock[buildID]["buildingEffectDesc"],
                            "UnlockDesc" :BuildUnlock[buildID]["buildingUnlockDesc"],
                        }
#########################################################################################################
# Weather
#########################################################################################################
WeatherData =SandboxEN["sandboxActTables"]["act1sandbox"]["weatherDatas"]

for weatherID in WeatherData.keys():
    WeatherDict[weatherID]={
                            "Name":WeatherData[weatherID]["name"],
                            "Type":WeatherData[weatherID]["weatherType"],
                            "TypeName":WeatherData[weatherID]["weatherTypeName"],
                            "Level":WeatherData[weatherID]["weatherLevel"],
                            "Function":WeatherData[weatherID]["functionDesc"],
                            "FunctionDetail" : SandboxEN["sandboxActTables"]["act1sandbox"]["runeDatas"][weatherID]["runes"][0]["blackboard"]
                        }

#########################################################################################################
# dumpling JSON
#########################################################################################################
dumpling=json.dumps({"Food":FoodDict,"Building":BuildDict,"Weather":WeatherDict},indent=4, ensure_ascii=False)
with open("temp/sandbox.json",'w') as JSON :
    JSON.write(dumpling)