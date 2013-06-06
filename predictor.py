import argparse
import shared
import sys
import subprocess


"""
parser = argparse.ArgumentParser(description='ProteinPrediction by Group 23 \n\
\n\
prediction program')
parser.add_argument('-p', metavar='wekapath', dest='WEKA_PATH', required=True, help='points to the weka executable e.g. /mnt/opt/data/pp1_13_exercise/weka-3-6-9/weka.jar')
parser.add_argument('-a', metavar='arff file', dest='arff', required=True, help='arff file for predictions')
args = parser.parse_args()
"""

input_file = "tmps_independent.arff"


try:
    with open(shared.MODEL_NAME):
        pass
except IOError:
    print "Create a model first. Use the model_creator.py!"
    sys.exit(1)
    

filtered_file = "pred_filtered.arff"

print "filter file ..."
subprocess.call(shared.filter_by_index(input_file, filtered_file))
print "predict ..."
result = subprocess.check_output(shared.load_model_command(shared.MODEL_NAME, filtered_file), shell=True).split('\n')


i = 0
for line in result:
    i += 1
    if i >= 6 and line.strip() != "":
        sys.stdout.write(line.split()[2][2])
        
        
