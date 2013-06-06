from __future__ import division
import subprocess
import operator
import time



WEKA_PATH = "/mnt/opt/data/pp1_13_exercise/weka-3-6-9/weka.jar"

#REMOVE_INDEX = "1-2707,2719-2885" # chemprop_hyd
REMOVE_INDEX = "1-81,502-1576,1578-2702,2724-2885" #pssm + chempop_hyd + helix
# 7 helix 5 A/R/N_pssm 6_chemprop_hyd
#REMOVE_INDEX = "1-181,185-201,205-221,225-241,245-261,265-281,285-301,305-321,325-341,345-361,365-381,385-1574,1590-2706,2720-2885"
INPUT_FILE = "tmps_X.arff"
FILE_COUNT = 3
FILTER_FILE = "filtered_X.arff"


def timer():
    while True:
        start = time.time()
        yield
        end = time.time()
        yield end - start
    


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump

def filter_command(in_, out, remove_index):
    return 'java -cp "' + WEKA_PATH + \
                '" weka.filters.unsupervised.attribute.Remove -R ' + \
                remove_index + ' -i '  + in_ + ' -o ' + out
                
        
def classify_command(train_in, test_in, c, gamma):
    return 'java -cp "' + WEKA_PATH + \
                '" weka.classifiers.functions.SMO -o -t ' + \
                train_in + ' -T ' + test_in + ' -C ' + str(c) + ' -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -K ' + \
                '"weka.classifiers.functions.supportVector.PolyKernel -C 250007 -E ' + str(gamma) + ' "'


""" 
    parses the weka output which is plain text 
    (perhaps there is a better format available???)
    output:
        number of right instances
        number of wrong instances
"""
def parse_classify_output(in_):
    for k,v in enumerate(in_):
        if v.find("Error on test data") != -1:
            return int(in_[k+2].split()[3]), int(in_[k+3].split()[3])
        
"""
    calculates how much instances are rightly classified
"""
def evaluate_classify_output(in_):
    true, false = parse_classify_output(in_)
    return true / (true + false)

                
def filter_files():         
    for i in range(0, FILE_COUNT):  
        in_ = INPUT_FILE.replace('X', str(i)) 
        out = FILTER_FILE.replace('X', str(i))
        subprocess.call(filter_command(in_, out, REMOVE_INDEX), shell=True)
    
    print "files filtered"
    
    

"""
  Classifies and searches for best c, gamma combination
  output: 
    results: a dictionary containing for each c, gamma tuple all results 
    (c, gamma) -> [{'test': 0.56, 'final': 0.83, 'testtime': 34.4, 'finaltime': 34.3}, ...] 
    
    best_combinations: a list containing the best combination for round 0,1 and 2 
"""
def classify():
    t = timer()
    results = {}
    best_combinations = []
    
    """ for all three starting files - find a new best combination """
    for i in range(0, FILE_COUNT):
        max_ = 0
        best_combination = ()
        print "round " + str(i)
        train_file = FILTER_FILE.replace("X", str(i))
        test_file = FILTER_FILE.replace("X", str((i + 1) % FILE_COUNT))
        final_test_file = FILTER_FILE.replace("X", str((i + 2) % FILE_COUNT))
        
        """ choose here your c, gamma range """
        c = -1
        while c <= 0:
        for c in frange(-1, 0, 0.2):
            for gamma in frange(-1, 2, 0.4):
                current_combination = (c, gamma)
                """ first round: create lists first """
                if i == 0:
                    results[current_combination] = []
                print current_combination
                
                t.next()
                test_result = subprocess.check_output(classify_command(train_file, test_file, c, gamma), shell=True).split('\n')
                et = t.next()
                print et
                test_percentage_right = evaluate_classify_output(test_result)
                print test_percentage_right
                
                results[current_combination].append({'test': test_percentage_right,
                                                     'testtime': et})
                
                 
                if test_percentage_right > max_:
                    best_combination = current_combination
        best_combinations.append(best_combination)
        best_c, best_gamma = best_combination
        print best_combination
        
        t.next()
        final_result = subprocess.check_output(classify_command(train_file, final_test_file, best_c, best_gamma), shell=True).split('\n')
        et = t.next()
        final_percentage_right = evaluate_classify_output(final_result) 
        print final_percentage_right
        print et
        results[best_combination][-1]['final'] = final_percentage_right   
        results[best_combination][-1]['finaltime'] = et   
        print results
    return results, best_combinations




""" 
  calculate the mean for all the best combinations
  using the three test values and the single final value of the current best combination
  i.e.: best_combination for round 0 is (c, gamma): take all three test values for (c, gamma)
        and the final value for round 0 for (c, gamma) and divide it by 4
"""
def calculate_mean(results, best_combinations):
    final_values = {}
    """ calculate a value for all the best combinations """
    for index, combination in enumerate(best_combinations):
        p = 0
        for i in range(0, FILE_COUNT):
            p = p + results[combination][i]['test']
            if i == index:
                p = p + results[combination][i]['final']
            
        c, gamma = combination
        final_values[(index, c, gamma)]  = p / (FILE_COUNT + 1)
    return final_values
    

filter_files()
results, best_combinations = classify()
final_values = calculate_mean(results, best_combinations)
print sorted(final_values.iteritems(), key=operator.itemgetter(1), reverse=True)


