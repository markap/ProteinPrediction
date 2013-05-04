from __future__ import division
import subprocess



WEKA_PATH = "C:\Program Files (x86)\Weka-3-6\weka.jar"

REMOVE_INDEX = "1-2707,2719-2885" # chemprop_hyd
# 7 helix 5 A/R/N_pssm 6_chemprop_hyd
REMOVE_INDEX = "1-181,185-201,205-221,225-241,245-261,265-281,285-301,305-321,325-341,345-361,365-381,385-1574,1590-2706,2720-2885"
INPUT_FILE = "tmps_X.arff"
FILE_COUNT = 3
FILTER_FILE = "filtered_X.arff"


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


def parse_classify_output(in_):
    for k,v in enumerate(in_):
        if v.find("Error on test data") != -1:
            return int(in_[k+2].split()[3]), int(in_[k+3].split()[3])
        
def evaluate_classify_output(in_):
    true, false = parse_classify_output(in_)
    return true / (true + false)

                
def filter_files():         
    for i in range(0, FILE_COUNT):  
        in_ = INPUT_FILE.replace('X', str(i)) 
        out = FILTER_FILE.replace('X', str(i))
        subprocess.call(filter_command(in_, out, REMOVE_INDEX), shell=True)
    
    print "files filtered"
    
    
#filter_files()


max_ = 0
max_c, max_gamma = 0, 0

for i in range(0, FILE_COUNT):
    print "round " + str(i)
    train_file = FILTER_FILE.replace("X", str(i))
    test_file = FILTER_FILE.replace("X", str((i + 1) % FILE_COUNT))
    final_test_file = FILTER_FILE.replace("X", str((i + 2) % FILE_COUNT))
    for c in frange(1, 2.1, 0.5):
        for gamma in frange(1, 1.1, 0.5):
            print c, gamma
            result = subprocess.check_output(classify_command(train_file, test_file, c, gamma), shell=True).split('\n')
            print evaluate_classify_output(result)
            if evaluate_classify_output(result) > max_:
                max_c, max_gamma = c, gamma
                
    result = subprocess.check_output(classify_command(train_file, final_test_file, c, gamma), shell=True).split('\n')
    r =parse_classify_output(result) 
    print max_c, max_gamma  
    print r
    print evaluate_classify_output(result)       




