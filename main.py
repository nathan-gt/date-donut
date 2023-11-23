import csv
import datetime
import glob
from math import floor
from random import randint, shuffle
import time

peeps = {0: {}} # empty dictionnary
GROUP_SIZE = 3
DONUTS = "donuts"
groups = []

def LoadDonutHistory():
    # Get latest save file in /saves
    list_of_files = glob.glob('saves/save-*.csv')
    maxTime = 0
    maxFile = ''
    for file in list_of_files:
        tempTime = int(file.removeprefix('saves\\save-').removesuffix('.csv'))
        if tempTime > maxTime:
            maxTime = tempTime
            maxFile = file
    if maxFile == '': maxFile = 'saves/save_clear.csv'

    # Load in the newest save
    with open(maxFile, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        i=0
        for row in reader:
            peeps[i] = {}
            peeps[i]['id'] = i
            peeps[i]['name'] = row['name']
            if row[DONUTS] != None and row[DONUTS] != "": peeps[i][DONUTS] = list(map(int, row[DONUTS].split('-')))
            else: peeps[i][DONUTS] = []
            i+=1

# util function to know if 2 ids in a group have already met, returns True or False
def HasNoConflict(group, id):
    for pers in group:
        if id in peeps[pers][DONUTS]: return False
    return True

def GenerateGroups(): 
    passedPeeps = []
    nbFullGroups = floor(len(peeps)/GROUP_SIZE)
    peepsRandArray = list(peeps.values()).copy() # this is to randomly iterate through the peeps without losing key bindings in the dictionary
    shuffle(peepsRandArray)
    for i in peeps:
        peep = peeps.get(peepsRandArray[i]['id'])
        if peep['id'] in passedPeeps: continue
        elif nbFullGroups == len(groups): # if there is still peeps to process but the max number of full groups is passed
            found = False
            for fullGroup in groups:
                if len(fullGroup) == GROUP_SIZE and HasNoConflict(fullGroup, peep): 
                    for pers in fullGroup: peeps[pers][DONUTS].append(i)
                    peep[DONUTS].extend(fullGroup)
                    fullGroup.append(peep['id'])
                    passedPeeps.append(peep['id'])
                    found = True
                    break
            if not found:
                print("Soft lock happened during execution due to insufficient available IDs, consider re-executing the program to try generating dates again")
                exit()
        else: # full group behavior
            group = [peep['id']]
            passedPeeps.append(peep['id'])
            for _ in range(GROUP_SIZE-1):
                id = -1
                if len(passedPeeps) != len(peeps) :
                    while (id < 0 or id in passedPeeps or id in peep[DONUTS] or not HasNoConflict(group, id) or id == peep['id']):
                        id = randint(0, len(peeps)-1)
                    group.append(id)
                    passedPeeps.append(id)
            
            groups.append(group)

            # for WriteOut(), update ['donuts'] for each group member
            for pers in group:
                temp = group.copy()
                temp.remove(pers)
                peeps[pers][DONUTS].extend(temp)

        if len(passedPeeps) == len(peeps) : 
            return
        
# updates the save
def WriteOut():
    with open('saves/save-'+str(floor(time.time()))+'.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'donuts']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in peeps:
            donutStr = ""
            for donut in peeps.get(i)['donuts']:
                donutStr += str(donut) + "-"
            writer.writerow({'name': peeps[i]['name'] , 'donuts': donutStr[:-1]})

def PrintGroups():
    for i in range(len(groups)):
        if (len(groups[i])>GROUP_SIZE): print("🍩 Date donut #"+str(i+1)+" (JUMBO) 🍩")
        elif (len(groups[i])<GROUP_SIZE): print("🍩 Date donut #"+str(i+1)+" (diet) 🍩")
        else: print("🍩 Date Donut #"+str(i+1)+" 🍩")
        for j in range(len(groups[i])):
            print("@"+ peeps[groups[i][j]]["name"])
        print("\n")

LoadDonutHistory()
GenerateGroups()
WriteOut()
print("\nDate donuts generated and written in saves/save.csv!\n")
PrintGroups()