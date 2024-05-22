


__author__ = "Ano"

import time
from inMemory.QPlusInMemoryWithConstraints import QPlusInMemoryWithConstraint
from inMemory.QPlusInMemoryWihtoutConstraints import QPlusInMemoryWithoutConstraint
from OnDisk.QPlusOnDiskWithConstraints import QPlusOnDiskWithConstraint
from OnDisk.QPlusOnDiskWithoutConstraints import QPlusOnDiskWithoutConstraint

###########################################################################
#                            main function                                #
###########################################################################

if __name__ == '__main__':
    print("##################################################################################")
    print("#                         Welcome to the QPlus Sampler !                         #")
    print("##################################################################################\n")

    
    datasets = ["retail", "BMS2", "kosarak", "chainstoreFIM", "USCensus"]
    algorithmsWC = {
        "QPlusInMemoryWithConstraint": QPlusInMemoryWithConstraint,
        "QPlusOnDiskWithConstraint": QPlusOnDiskWithConstraint
    }
    keyWC = {
        '1': "QPlusInMemoryWithConstraint",
        '2': "QPlusOnDiskWithConstraint"
    }
    algorithmsWOC = {
        "QPlusInMemoryWithoutConstraint": QPlusInMemoryWithoutConstraint,
        "QPlusOnDiskWithoutConstraint": QPlusOnDiskWithoutConstraint
    }
    keyW0C = {
        '1': "QPlusInMemoryWithoutConstraint",
        '2': "QPlusOnDiskWithoutConstraint"
    }
    
    print("Available datasets:", [str((i+1))+":"+datasets[i] for i in range(len(datasets))])
    name = datasets[int(input("Choose a dataset: "))-1]
    if name not in datasets:
        print("Invalid dataset choice.")
        exit()
    
    algorithm_choice = input("Choose an algorithm (1:with or 0:without constraint): ")
    if algorithm_choice == '1':
        constrained = True
    elif algorithm_choice == '0':
        constrained = False
    else:
        print("Invalid algorithm choice.")
        exit()

    max_Length = 0
    algorithm_function = ''
    if constrained:
        max_Length = int(input("Enter maximal length constraint: "))
        print("Available algorithms:")
        i = 1
        for alg in keyWC.keys():
            print("\t",str(i)+":"+keyWC[alg])
            i += 1
        algorithm_choice = input("Choose an algorithm: ")
        if algorithm_choice not in keyWC.keys():
            print("Invalid algorithm choice.")
            exit()
        algorithm_function = algorithmsWC[keyWC[algorithm_choice]]
    else:
        print("Available algorithms:")
        i = 1
        for alg in keyW0C.keys():
            print("\t",str(i)+":"+keyW0C[alg])
            i += 1
        algorithm_choice = input("Choose an algorithm: ")
        if algorithm_choice not in keyW0C:
            print("Invalid algorithm choice.")
            exit()
        algorithm_function = algorithmsWOC[keyW0C[algorithm_choice]]

    N = int(input("Enter the desired sample size: "))
    
    dataset = "../DatasetsHUI/" + name + ".num"
    
    beginTime = time.time()
    sampledPatterns = algorithm_function(dataset, ":", max_Length, N)
    endTime = time.time() - beginTime
    print("Execution time (s):", endTime)
    del sampledPatterns
    
    
    print("##################################################################################")
    print("#                             Thanks for using QPlus !                           #")
    print("##################################################################################\n")
