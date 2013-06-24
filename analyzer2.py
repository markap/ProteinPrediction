from __future__ import division
import time
import sys
import predictor
import model_creator


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
  Classifies and searches for best c, gamma combination
  output: 
    results: a dictionary containing for each c, gamma tuple all results 
    (c, gamma) -> [{'test': 0.56, 'final': 0.83, 'testtime': 34.4, 'finaltime': 34.3}, ...] 
    
    best_combinations: a list containing the best combination for round 0,1 and 2 
"""
def classify():
    t = timer()
            
    """ choose here your c, gamma range """
    for c in frange(0.1, 1.5, 0.1):
        #c = 32;
        for gamma in frange(0.1, 1.5, 0.1):
            
            print "### combination ###"
            print c, gamma
            
            
            print "### build model ###"
            sys.stdout.flush()
            t.next()
            model_creator.build_model("tmps.arff", c, gamma)
            sys.stdout.flush()
            print t.next()
            print "### predict ###"
            t.next()
            predictor.predict("tmps_independent.arff")
            print t.next()
            sys.stdout.flush()
           
           
print done