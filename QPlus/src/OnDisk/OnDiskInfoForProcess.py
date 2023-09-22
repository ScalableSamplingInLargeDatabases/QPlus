
###########################################################################
#                           loading functions                             #
###########################################################################

def load_dataset_OnDisk(dataset, delim):
    data = []
    maxItemsetLength = 0
    with open(dataset, 'r') as base:
        line = base.readline()
        while line:
            w_trans = 0
            trans = line.split()
            lentrans = len(trans)
            for info in trans:
                info = info.split(delim)
                w_trans += float(info[1])
            data.append((lentrans, w_trans))
            maxItemsetLength = max(maxItemsetLength, lentrans)
            line = base.readline()
    return data, maxItemsetLength

