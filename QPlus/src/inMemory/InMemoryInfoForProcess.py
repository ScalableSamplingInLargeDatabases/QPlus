
import json

###########################################################################
#                           loading FunctionsWithConstraints                             #
###########################################################################

def load_dataset_inMemory(dataset, delim):
    data = []
    maxItemsetLength = 0
    with open(dataset, 'r') as base:
        line = base.readline()
        while line:
            itemset = []
            w_trans = 0
            for info in line.split():
                info = info.split(delim)
                w_trans += float(info[1])
                itemset.append((info[0], w_trans))
            data.append(itemset)
            maxItemsetLength = max(maxItemsetLength, len(itemset))
            line = base.readline()
    return data, maxItemsetLength

def load_profile_inMemory(dataset):
    dico_items = {}
    f = open(dataset)
    dataProfile = json.load(f)
    q_database = {}
    for e in dataProfile['links']:
        if str((e['subset_of_source'], e['value'], e['subset_of_target'])) not in dico_items.keys():
            dico_items[str((e['subset_of_source'], e['value'], e['subset_of_target']))] = str(len(dico_items) + 1)
        item = dico_items[str((e['subset_of_source'], e['value'], e['subset_of_target']))]
        
        if e['source'] + "_s" in q_database.keys():
            q_database[e['source'] + "_s"].append((item, e['stat']))
        else:
            q_database[e['source'] + "_s"] = [(item, e['stat'])]

        if e['target'] + "_o" in q_database.keys():
            q_database[e['target'] + "_o"].append((item, e['stat']))
        else:
            q_database[e['target'] + "_o"] = [(item, e['stat'])]

    data = []
    maxItemsetLength = 0
    for e in q_database:
        itemset = []
        w_trans = 0
        for info in q_database[e]:
            w_trans += float(info[1])
            itemset.append([info[0], w_trans])
        data.append(itemset)
        maxItemsetLength = max(maxItemsetLength, len(itemset))
    return data, maxItemsetLength

