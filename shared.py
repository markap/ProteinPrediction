"""
   contains commands and constants used throughout the whole application
"""


#WEKA_PATH = "/mnt/opt/data/pp1_13_exercise/weka-3-6-9/weka.jar"
WEKA_PATH = "C:\Program Files (x86)\Weka-3-6\weka.jar"

#REMOVE_INDEX = "1-2707,2719-2885" # chemprop_hyd
REMOVE_INDEX = "1-81,502-1576,1578-2702,2724-2885" #pssm + chempop_hyd + helix
# 7 helix 5 A/R/N_pssm 6_chemprop_hyd
#REMOVE_INDEX = "1-181,185-201,205-221,225-241,245-261,265-281,285-301,305-321,325-341,345-361,365-381,385-1574,1590-2706,2720-2885"

MODEL_NAME = 'smo.model'


def filter_by_index(in_, out):
    return filter_command(in_, out, REMOVE_INDEX)


def filter_command(in_, out, remove_index):
    return 'java -cp "' + WEKA_PATH + \
                '" weka.filters.unsupervised.attribute.Remove -R ' + \
                remove_index + ' -i '  + in_ + ' -o ' + out
                
                
def classify_command(train_in, test_in, c, gamma):
    return 'java -cp "' + WEKA_PATH + \
                '" weka.classifiers.functions.SMO -o -t ' + \
                train_in + ' -T ' + test_in + ' -C ' + str(c) + ' -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -K ' + \
                '"weka.classifiers.functions.supportVector.PolyKernel -C 250007 -E ' + str(gamma) +  ' "'
                

        
def store_model_command(train_in, model_out, c, gamma):
    return 'java -cp "' + WEKA_PATH + \
                '" weka.classifiers.functions.SMO -o -no-cv -t ' + \
                train_in + ' -T ' + train_in + ' -d  ' + model_out + ' -C ' + str(c) + ' -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -K ' + \
                '"weka.classifiers.functions.supportVector.PolyKernel -C 250007 -E ' + str(gamma) + ' "'





def load_model_command(model_in, test_in):
    return 'java -cp "' + WEKA_PATH + \
                '" weka.classifiers.functions.SMO -o -l ' + \
                model_in + ' -T ' + test_in + ' -p 0'
                