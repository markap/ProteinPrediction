import argparse
import shared
import sys
import subprocess




parser = argparse.ArgumentParser(description='ProteinPrediction by Group 23 \n\
\n\
prediction program')
parser.add_argument('-a', metavar='arff file', dest='arff', required=True, help='arff file for predictions')
args = parser.parse_args()

input_file = args.arff

try:
    with open(args.arff): pass
except IOError:
    print 'Specified arff file does not exist!'
    sys.exit(1)
try:
    with open(shared.MODEL_NAME): pass
except IOError:
    print "Create a model first. Use the model_creator.py!"
    sys.exit(1)


file_handle = open(input_file, "r")
header_mode = True
protein_key = ''

result = []


count = 0
for line in file_handle:
    
    
    if header_mode == False:
        
        count += 1

        s = line[0:(line.find(','))]
        current_protein_key = s[0:(s.rfind('_'))]
       
        if current_protein_key != protein_key:
            if protein_key != "":
                result.append({'protein': protein_key, 'residues': count})
          
            protein_key = current_protein_key         
            count = 0
       
            
    if line.strip() == '@DATA':
        header_mode = False
    
file_handle.close()
print result
    

filtered_file = "pred_filtered.arff"

print "filter file ..."
subprocess.call(shared.filter_by_index(input_file, filtered_file), shell=True)
print "predict ..."
result = subprocess.check_output(shared.load_model_command(shared.MODEL_NAME, filtered_file), shell=True).split('\n')


i = 0
protein_index = 0
prediction_index = 0
current_protein = None
for line in result:
    i += 1
    if i >= 6 and line.strip() != "":
        current_protein = result[protein_index]
        if prediction_index == 0:
            print current_protein['protein']
        prediction_index += 1
        sys.stdout.write(line.split()[2][2])
        if prediction_index == current_protein['residues']:
            prediction_index = 0
            print ""
        
      
