
result = 'result'

original_file = 'tmps_independent.arff'

file_handle = open(result, "r")

predictions = []

for line in file_handle:
    if line.find('>') == -1:
	   predictions += list(line.strip())


file_handle.close()

file_handle = open(original_file, "r");

header_mode = True

right = 0.0
wrong = 0.0
tp = 0.0
tn = 0.0
fp = 0.0
fn = 0.0

i = 0
for line in file_handle:
    if header_mode == False:
        original_value = line.strip()[-1:]
	    
        predicted_value = predictions[i]
	
       
    
    	if original_value == predicted_value:
            if original_value == "+":
                tp += 1
            else:
                tn += 1
    	    right += 1
    	else:
    	    wrong += 1
            if predicted_value == "+":
                fp += 1
            else:
                fn += 1

	i += 1
        
            
    if line.strip() == '@DATA':
        header_mode = False
 	

file_handle.close()

print right
print wrong
	

acc = right / (right + wrong)
acc2 = tp+tn /(tp+tn+fp+fn)

acc_pos = tp / (tp+fp)
cov_pos = tp / (tp+fn)
acc_neg = tn / (tn+fn)
cov_neg = tn / (tn+fp)

print acc, acc2, acc_pos, cov_pos, acc_neg, cov_neg
    
