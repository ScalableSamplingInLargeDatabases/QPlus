__author__ = "Ano"

import os

import time
from inMemory.QPlusInMemoryWithConstraints import QPlusInMemoryWithConstraint, QPlusInMemoryWithConstraintProfile
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


    datasets = ["retail", "BMS2", "kosarak", "chainstoreFIM", "USCensus", "T50I10D2M"]
    profil_datasets = ["DOREMUS", "BENICULTURALI", "DBPEDIA"]
    
    profil_datasets = []
    
    dossier = "../DatasetsHUI/Profiles/"
    for nom_fichier in os.listdir(dossier):
        chemin_fichier = os.path.join(dossier, nom_fichier)
        if os.path.isfile(chemin_fichier) and nom_fichier.endswith("_Profile.json"):
            profil_datasets.append(nom_fichier)

    dataset_profile = ''
    dataset_type = input("Choose your dataset type (1:Knowledge graph Profile or 0: None-semantic quantitative database): ")
    if dataset_type == '1':
        dataset_profile = True
    elif dataset_type == '0':
        dataset_profile = False
    else:
        print("Invalid type choice.")
        exit()
    sampledPatterns, preprocessingTime, samplingTime = {}, 0, 0
    executionTime = 0
    if not dataset_profile:
        print("Available datasets:", [str((i+1))+":"+datasets[i] for i in range(len(datasets))])
        name = datasets[int(input("Choose a dataset: "))-1]
        if name not in datasets:
            print("Invalid dataset choice.")
            exit()
        dataset = "../DatasetsHUI/" + name + ".num"

        constrained = ''
        algorithm_choice = input("Choose an algorithm (1:with or 0:without constraint): ")
        if algorithm_choice == '1':
            constrained = True
        elif algorithm_choice == '0':
            constrained = False
        else:
            print("Invalid algorithm choice.")
            exit()

        N = int(input("Enter the desired sample size: "))
        delim = ':'
        if constrained:
            max_Length = int(input("Enter maximal length constraint: "))

            algorithmsWC = {
                "QPlusInMemoryWithConstraint": QPlusInMemoryWithConstraint,
                "QPlusOnDiskWithConstraint": QPlusOnDiskWithConstraint
            }

            keyWC = {
                '1': "QPlusInMemoryWithConstraint",
                '2': "QPlusOnDiskWithConstraint"
            }
            print("Available algorithms:")
            i = 1
            for alg in keyWC.keys():
                print("\t",str(i)+":"+keyWC[alg])
                i += 1
            algorithm_choice = input("Choose an algorithm: ")
            if algorithm_choice not in keyWC.keys():
                print("Invalid algorithm choice.")
                exit()

            print(keyWC[algorithm_choice])
            beginTime = time.time()
            sampledPatterns, preprocessingTime, samplingTime = algorithmsWC[keyWC[algorithm_choice]](dataset, delim, max_Length, N)
            executionTime = time.time() - beginTime

        else:
            algorithmsWOC = {
                "QPlusInMemoryWithoutConstraint": QPlusInMemoryWithoutConstraint,
                "QPlusOnDiskWithoutConstraint": QPlusOnDiskWithoutConstraint
            }


            keyW0C = {
                '1': "QPlusInMemoryWithoutConstraint",
                '2': "QPlusOnDiskWithoutConstraint"
            }
            print("Available algorithms:")
            i = 1
            for alg in keyW0C.keys():
                print("\t",str(i)+":"+keyW0C[alg])
                i += 1
            algorithm_choice = input("Choose an algorithm: ")
            if algorithm_choice not in keyW0C:
                print("Invalid algorithm choice.")
                exit()
            print(keyW0C[algorithm_choice])
            beginTime = time.time()
            sampledPatterns, preprocessingTime, samplingTime = algorithmsWOC[keyW0C[algorithm_choice]](dataset, delim, N)
            executionTime = time.time() - beginTime
    else:
        print("Available datasets RDF Profiles:", [str((i+1))+":"+profil_datasets[i] for i in range(len(profil_datasets))])
        name = profil_datasets[int(input("Choose a dataset: "))-1]
        if name not in profil_datasets:
            print("Invalid dataset choice.")
            exit()
        dataset = os.path.join(dossier, name)# "../DatasetsHUI/Profiles/" + name + "_Profile.json"

        N = int(input("Enter the desired sample size: "))
        if N<0:
            print("Invalid sample size.")
            exit()
        delim = ':'
        max_Length = int(input("Enter maximal length constraint: "))
        if max_Length<0:
            print("Invalid maximal length constraint.")
            exit()
        i = 1
        for name in profil_datasets:
            print(name, i,"/",len(profil_datasets))
            i += 1
            dataset = os.path.join(dossier, name)
            beginTime = time.time()
            sampledPatterns, preprocessingTime, samplingTime = QPlusInMemoryWithConstraintProfile(dataset, max_Length, N)
            executionTime = time.time() - beginTime
            print("\tPreprocessing time (s)   :", preprocessingTime)
            print("\tSampling time (s)        :", samplingTime)
            print("\tDistinct sampled patterns:", len(sampledPatterns))
            print("Execution time (s):", executionTime)

    print("##################################################################################")
    print("#                             Thanks for using QPlus !                           #")
    print("##################################################################################\n")
    #print(sampledPatterns)


