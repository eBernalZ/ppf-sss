import subprocess
python_executable = "python3"

S = {200: [25, 50, 100],     
    10000: [25, 50, 100],     
    1000000: [25, 50, 100]}

NOBJ = range(2, 11)


instances = {
            "ZCAT1": {"nobj": NOBJ, "cardinality": S}, "ZCAT2": {"nobj": NOBJ, "cardinality": S},
            "ZCAT3": {"nobj": NOBJ, "cardinality": S}, "ZCAT4": {"nobj": NOBJ, "cardinality": S},
            "ZCAT5": {"nobj": NOBJ, "cardinality": S}, "ZCAT6": {"nobj": NOBJ, "cardinality": S},
            "ZCAT7": {"nobj": NOBJ, "cardinality": S}, "ZCAT8": {"nobj": NOBJ, "cardinality": S},
            "ZCAT9": {"nobj": NOBJ, "cardinality": S}, "ZCAT10": {"nobj": NOBJ, "cardinality": S}, 
            "ZCAT11": {"nobj": NOBJ, "cardinality": S}, "ZCAT12": {"nobj": NOBJ, "cardinality": S}, 
            "ZCAT13": {"nobj": NOBJ, "cardinality": S}, "ZCAT14": {"nobj": NOBJ, "cardinality": S},
            "ZCAT15": {"nobj": NOBJ, "cardinality": S}, "ZCAT16": {"nobj": NOBJ, "cardinality": S},
            "ZCAT17": {"nobj": NOBJ, "cardinality": S}, "ZCAT18": {"nobj": NOBJ, "cardinality": S},
            "ZCAT19": {"nobj": NOBJ, "cardinality": S}, "ZCAT20": {"nobj": NOBJ, "cardinality": S}
            } 

algorithms = {#"inclusion": {"exec": 1, "is_randomized": False, "samples": "same_as_subset"}, 
            "rand_inclusion": {"exec": 20, "is_randomized": True, "samples": "same_as_subset"}, 
            "rand_removal": {"exec": 20, "is_randomized": True, "samples": "same_as_subset"}, 
            "iterative": {"exec": 20, "is_randomized": True, "cycles": "user_defined"}}

distance = "euclidean"
PPF = "RSE"

for alg in algorithms:
    exec = algorithms[alg]["exec"]
    for instance in instances:
        for nobj in instances[instance]["nobj"]:
            cardinality_dict = instances[instance]["cardinality"]
            for M in cardinality_dict:
                instance_name = "{0}_{1}".format(instance, M)
                for subset_size in cardinality_dict[M]:                   

                    if algorithms[alg]["is_randomized"]:
                        if alg == "iterative" and algorithms[alg]["cycles"] == "user_defined":
                            cycles = str(10000) # AVOID HARD-CODING.
                            #cycles = str(M)
                            execution_line = [python_executable, "reduce.py", PPF, alg,                                
                                                cycles, 
                                                instance_name, 
                                                str(nobj), 
                                                str(subset_size), 
                                                str(exec), 
                                                distance]   
                        else:
                            if algorithms[alg]["samples"] == "same_as_subset":
                                samples = str(subset_size)
                                execution_line = [python_executable, "reduce.py", PPF, alg,                                
                                                samples, 
                                                instance_name, 
                                                str(nobj), 
                                                str(subset_size), 
                                                str(exec), 
                                                distance]                
                    else:                        
                        execution_line = [python_executable, "reduce.py", PPF, alg,
                                        instance_name, 
                                        str(nobj), 
                                        str(subset_size), 
                                        str(exec), 
                                        distance]
                    subprocess.run(execution_line, shell=False)

