import csv
import datetime
import glob
from math import floor
from random import randint, shuffle
import time
from copy import deepcopy

peeps = {0: {}} # empty dictionnary
peepsCopy = {0: {}} # empty dictionnary to be used to keep the original loaded peeps
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
            peepsCopy[i] = {}
            peepsCopy[i]['id'] = i
            peepsCopy[i]['name'] = row['name']
            if row[DONUTS] != None and row[DONUTS] != "": peepsCopy[i][DONUTS] = list(map(int, row[DONUTS].split('-')))
            else: peepsCopy[i][DONUTS] = []
            i+=1

# util function to know if 2 ids in a group have already met, returns True or False
def HasNoConflict(group, id):
    for pers in group:
        if id in peeps[pers][DONUTS]: return False
    return True

def GenerateGroups(): 
    passedPeeps = []
    global groups
    global peeps
    global peepsCopy
    groups = []
    peeps = deepcopy(peepsCopy)
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
                groups = []
                return False # There is no possible group with the ids left
        else: # full group behavior
            group = [peep['id']]
            passedPeeps.append(peep['id'])
            for _ in range(GROUP_SIZE-1):
                id = -1
                if len(passedPeeps) != len(peeps) : 
                    if len(peeps) - len(passedPeeps) <= len(peep[DONUTS]): # try to choose an id when it's possible there are no options left
                        for p in peepsRandArray:
                            if p['id'] in passedPeeps or p['id'] == peep['id'] or not HasNoConflict(group, p['id']): continue
                            else:
                                id = p['id']
                                break;
                        if id == -1 : 
                            groups = []
                            return False # There is no possible group with the ids left
                    else: 
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
            return True
    return True
        
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
while not GenerateGroups(): 
    print("Stumbled upon an impossible generation, attempting automatic retry")
    continue
WriteOut()
print("\nDate donuts generated and written in ./saves/ !\n")
PrintGroups()