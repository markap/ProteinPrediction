

def evaluate(predictions):

    file_handle = open(original_file, "r");

    header_mode = True

    right = 0.0
    wrong = 0.0

    i = 0
    for line in file_handle:
        if header_mode == False:
	    original_value = line.strip()[-1:]
	
	    predicted_value = predictions[i]

	    if original_value == predicted_value:
	        right += 1
	    else:
	        wrong += 1

	    i += 1
        
            
        if line.strip() == '@DATA':
            header_mode = False
 	

    file_handle.close()

    #print right
    #print wrong
	

    return right / (right + wrong)


import heapq

result = 'nohup.out'

original_file = 'tmps_independent.arff'

file_handle = open(result, "r")

predictions = []

best = []


for line in file_handle:
    if line.find('### combination') != -1:
        predict = False
        combination = True
	if len(predictions) > 0:
            acc = evaluate(predictions)
            print acc
            predictions = []
            heapq.heappush(best, (1-acc, (combinations, time, acc)))
    elif combination == True:
        combination = False
        print line.strip()
        combinations = line.strip()

    if line.find('### predict') != -1:
        predict = True
    elif predict == True and (line[0] == '+' or line[0] == '-'):
	predictions += list(line.strip())
    elif predict == True and line[0] != '>':
        print line.strip()
        time = line.strip()



file_handle.close()


print heapq.heappop(best)
