from __future__ import division
import subprocess
import operator
import time
import shared
import sys


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
    parses the weka output which is plain text
    (perhaps there is a better format available???)
    output:
        tp = True Positive
        fp = False Positive
        fn = False Negative
        tn = True Negative
"""
def parse_classify_ConfMatr(in_):
    for k,v in enumerate(in_):
        if v.find("Error on test data") != -1:
            return int(in_[k+15].split()[0]), int(in_[k+15].split()[1]), int(in_[k+16].split()[0]),int(in_[k+16].split()[1])


            """
    calculates how much instances are rightly classified
"""
def evaluate_classify_ConfMatr(in_):
    tp, fp, fn, tn = parse_classify_ConfMatr(in_)
    acc_pos = tp / (tp+fp)
    cov_pos = tp / (tp+fn)
    acc_neg = tn / (tn+fn)
    cov_neg = tn / (tn+fp)
    return acc_pos, cov_pos, acc_neg, cov_neg


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
        subprocess.call(shared.filter_by_index(in_, out), shell=True)
    
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
        for c in frange(0.1, 1.5, 0.1):
            #c = 32;
            for gamma in frange(0.1, 1.5, 0.1):
                #gamma = 2**(-11);
                current_combination = (c, gamma)
                """ first round: create lists first """
                if i == 0:
                    results[current_combination] = []
                print current_combination
		sys.stdout.flush()
                
                t.next()
                test_result = subprocess.check_output(shared.classify_command(train_file, test_file, c, gamma), shell=True).split('\n')
                et = t.next()
                print et
                test_percentage_right = evaluate_classify_output(test_result)
                #prints acc_pos,cov_pos,acc_neg,cov_neg
                print evaluate_classify_ConfMatr(test_result)
                #prints Q2
                print test_percentage_right
                
                results[current_combination].append({'test': test_percentage_right,
                                                     'testtime': et})
                
                 
                if test_percentage_right > max_:
                    best_combination = current_combination

	sys.stdout.flush()
        best_combinations.append(best_combination)
        best_c, best_gamma = best_combination
        print best_combination
        
        t.next()
        final_result = subprocess.check_output(shared.classify_command(train_file, final_test_file, best_c, best_gamma), shell=True).split('\n')
        et = t.next()
        final_percentage_right = evaluate_classify_output(final_result) 
        #prints acc_pos,cov_pos,acc_neg,cov_neg
        print evaluate_classify_ConfMatr(final_result)
        #prints Q2
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
    


print "filter files"
filter_files()
results, best_combinations = classify()
final_values = calculate_mean(results, best_combinations)
print sorted(final_values.iteritems(), key=operator.itemgetter(1), reverse=True)
