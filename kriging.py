
import numpy as np
from sys import argv, exit
import time,operator
from sklearn import cross_validation

def normalizeDataset(train, test):
	for att in ('age', 'account_value', 'withdrawal_rate', 'maturity'):
		mu = np.mean(train[att])
		sigma = np.std(train[att])
		train[att] = normalize(train[att], mu, sigma)
		test[att] = normalize(test[att], mu, sigma)


def normalize(arr, mu, sigma):
	return (arr-mu)/sigma



def train_and_test(X_train,Y_train,X_test,Y_test,dtype,alpha,beta_percentile,cv=True):
	k = X_train.shape[0]
	n = X_test.shape[0]

	A = np.zeros(shape=(k,k))
	lambd = 1
	part1 = np.column_stack((X_train['guarantee_type'], X_train['gender']))
	part2 = np.column_stack((X_train['age'], X_train['account_value'], X_train['withdrawal_rate'],X_train['maturity']))

	for i in range(k):
		tmp = np.array([X_train[i],]*k, dtype=dtype)	
		tmp1 = np.column_stack((tmp['guarantee_type'], tmp['gender']))	#copy this row k times
		tmp2 = np.column_stack((tmp['age'], tmp['account_value'], tmp['withdrawal_rate'],tmp['maturity']))
		result1 = lambd*np.sum(np.bitwise_xor(part1, tmp1), axis=1)
		result2 = np.sum((part2-tmp2)**2,axis=1)
		A[i] = np.sqrt(result1+result2)

	# tmp = np.triu(A)
	# tmp = tmp[tmp!=0]
	max_dist = A.max()
	B = np.zeros(shape=(k+1,k+1))
	B[k] = B[:,k] = 1
	B[k,k] = 0	

	part1 = np.column_stack((X_test['guarantee_type'], X_test['gender']))
	part2 = np.column_stack((X_test['age'], X_test['account_value'], X_test['withdrawal_rate'],X_test['maturity']))

	weight_mat = np.zeros((k+1,n))
	weight_mat[k] = 1
	beta = max_dist*beta_percentile

	for j in range(k):
		B[j][:k] = alpha+np.exp(-3*A[j]/beta)	
		tmp = np.array([X_train[j],]*n, dtype=dtype)	
		tmp1 = np.column_stack((tmp['guarantee_type'], tmp['gender']))	#copy this row k times
		tmp2 = np.column_stack((tmp['age'], tmp['account_value'], tmp['withdrawal_rate'],tmp['maturity']))
		result1 = lambd*np.sum(np.bitwise_xor(part1, tmp1), axis=1)
		result2 = np.sum((part2-tmp2)**2,axis=1)
		weight_mat[j] = alpha+np.exp(np.sqrt(result1+result2)*(-3/beta))

	Y_train = np.append(Y_train, 0)
	const = np.dot(np.linalg.inv(B),Y_train)
	Y_hat = np.dot(const, weight_mat)
	
	if cv == True:
		RMSE = np.sqrt(sum((Y_test-Y_hat)**2)/n)
		return RMSE
	else:
		RMSE = np.sqrt(sum((Y_test-Y_hat)**2)/(n+k))
		MAD = sum(abs(Y_test-Y_hat))/(n+k)
		total = sum(Y_hat)+sum(Y_train)
		benchmark = sum(Y_test)+sum(Y_train)
		APD = abs(total-benchmark)
		RPD = APD/benchmark	
		return APD,RPD,MAD,RMSE



def crossValidation(X_train_orig,Y_train_orig,dtype):
	n = X_train_orig.shape[0]                               
	beta_percentile_arr = [0.5,1,1.5,2,2.5,3]
	cv_result = {}
	np.random.seed(0)

	for j in range(len(beta_percentile_arr)):
		kf = cross_validation.KFold(n, n_folds=5, shuffle=True)
		RMSE = 0

		for train_index, test_index in kf:
			X_train, X_test = X_train_orig[train_index], X_train_orig[test_index]
			Y_train, Y_test = Y_train_orig[train_index], Y_train_orig[test_index]
			RMSE += train_and_test(X_train,Y_train,X_test,Y_test,dtype,0,beta_percentile_arr[j])

		cv_result[beta_percentile_arr[j]] = RMSE/5
		print(str(beta_percentile_arr[j])+","+str(RMSE/5)+"\n")
		
	sorted_cv_result = sorted(cv_result.iteritems(), key=operator.itemgetter(1))		
	return sorted_cv_result[0][0]		


def main():
	if len(argv) != 2:
		print("input a folder")
		exit(1)	

	folder = argv[1]
	trainingDataName = folder + "/random_train.csv"
	testingDataName = folder + "/random_test.csv"

	dtype=[('guarantee_type', '<i4'), ('gender', '<i4'), ('age', '<f8'), ('account_value', '<f8'), ('withdrawal_rate', '<f8'), ('maturity', '<f8')]

	X_train = np.genfromtxt(trainingDataName, delimiter=',', dtype=dtype, usecols=[2,3,4,5,6,7])
	Y_train = np.loadtxt(trainingDataName, delimiter=',', usecols=[0])

	X_test = np.genfromtxt(testingDataName, delimiter=',', dtype=dtype, usecols=[2,3,4,5,6,7])
	Y_test = np.loadtxt(testingDataName, delimiter=',', usecols=[0])

	normalizeDataset(X_train, X_test)
	start_time = time.clock() #start time of the program
	beta = crossValidation(X_train,Y_train,dtype)
	print(str(beta))
	#start_time = time.clock() #start time of the program
	#APD,RPD,MAD,RMSE = train_and_test(X_train,Y_train,X_test,Y_test,dtype,0,beta,False)	
	#print(str(time.clock() - start_time))
	#print(str(RPD))
	#output = np.array([APD,RPD,MAD,RMSE])
	#np.savetxt(folder+"/kriging_random_results.csv", output.reshape(1, output.shape[0]),fmt="%12.5f",delimiter=",")


if __name__ == "__main__":
	main()
