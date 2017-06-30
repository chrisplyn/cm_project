from svmutil import *
import numpy as np
from sys import argv, exit
import time,operator

def normalizeDataset(x_train, x_test=None):	
	for att in ('age', 'account_value', 'withdrawal_rate', 'maturity'):
		mu = np.mean(x_train[att])
		sigma = np.std(x_train[att])
		x_train[att] = normalize(x_train[att], mu, sigma)
		if x_test is not None:
			x_test[att] = normalize(x_test[att], mu, sigma)


def normalize(arr, mu, sigma):
	return (arr-mu)/sigma



def cross_validation_param(c_begin, c_end, c_step, gamma_begin, gamma_end, gamma_step):
	dtype = 'float32'
	cost = np.power(2,np.arange(c_begin, c_end+c_step, c_step),dtype=dtype)	
	gamma = np.power(2,np.arange(gamma_begin, gamma_end+gamma_step, gamma_step),dtype=dtype)
	return cost,gamma


def split_data(data):
	part1 = np.column_stack((data['guarantee_type'], data['gender']))
	part2 = np.column_stack((data['age'], data['account_value'], data['withdrawal_rate'],data['maturity']))	
	return part1,part2


def get_training_kernel(X_train, part1, part2, gamma, lambd,dtype):
	k = X_train.shape[0]
	training_kernel = np.empty((k,k+1))
	
	for i in range(k):
		tmp = np.array([X_train[i],]*k, dtype=dtype)	
		tmp1,tmp2 = split_data(tmp)
		result1 = lambd*np.sum(np.bitwise_xor(part1, tmp1), axis=1)
		result2 = np.sum((part2-tmp2)**2,axis=1)
		training_kernel[i,1:] = np.exp((result1+result2)*(-gamma))
	training_kernel[:,0] = np.arange(k)+1
	return 	training_kernel.tolist()


def cross_validiation(X_train,part1,part2,Y_train,lambd,dtype):
	cost = [10.0, 31.6227766017, 100.0, 316.227766017, 1000.0, 3162.27766017, 10000.0, 31622.7766017, 100000.0]
	gamma =  [1e-08, 1e-07, 1e-06, 1e-05, 0.0001, 0.001, 0.01, 0.1, 1.0] 
	cv_result = {}

	for g in gamma:
		training_kernel = get_training_kernel(X_train,part1,part2,g,lambd,dtype)

		for c in cost:
			param_list = '-s 3 -t 4 -v 5 -q -c '+str(c)
			svm_param = svm_parameter(param_list)
			prob = svm_problem(Y_train, training_kernel, isKernel=True)
			cv_acc = svm_train(prob, svm_param)
			cv_result[(c, g)] = cv_acc

	sorted_cv_result = sorted(cv_result.iteritems(), key=operator.itemgetter(1))		
	best_param = sorted_cv_result[0]
	return best_param[0][0], best_param[0][1]


def svm_prediction(X_train, X_test,svm_model, gamma, lambd, dtype, Y_test=None):
	n = X_test.shape[0] 
	k = X_train.shape[0]
	part1,part2 = split_data(X_test)
	testing_kernel = np.empty((n,k+1))

	for j in range(k):
		tmp = np.array([X_train[j],]*n, dtype=dtype)	
		tmp1,tmp2 = split_data(tmp)
		result1 = lambd*np.sum(np.bitwise_xor(part1, tmp1), axis=1)
		result2 = np.sum((part2-tmp2)**2,axis=1)
		testing_kernel[:,j+1] = np.exp((result1+result2)*(-gamma))
	
	testing_kernel[:,0] = np.arange(n)+1
	testing_kernel = testing_kernel.tolist()
	if Y_test is not None:
		p_labels, p_acc, p_vals = svm_predict(Y_test, testing_kernel, svm_model)	
	else:
		p_labels, p_acc, p_vals = svm_predict([0]*len(testing_kernel), testing_kernel, svm_model)
	return 	p_labels, p_acc



def main():
	if len(argv) != 3:
		print("input a folder, and test_flag value")
		exit(1)	

	folder = argv[1]
	test_flag = argv[2]
	trainingDataName = folder + "/training_processed.csv"
	testingDataName = folder + "/testing_processed.csv"
	lambd = 1

	'''Part I:
	Read data, X_train, Y_train, X_test, Y_test,
	then normalize  the numerical those features in both training and testing data.
	When normalizing the testing data, use mean and std of corresponding features calcualted from training data
	'''
	dtype=[('guarantee_type', '<i4'), ('gender', '<i4'), ('age', '<f8'), ('account_value', '<f8'), ('withdrawal_rate', '<f8'), ('maturity', '<f8')]
	X_train = np.loadtxt(trainingDataName, delimiter=',', dtype=dtype, usecols=[2,3,4,5,6,7])
	Y_train = np.loadtxt(trainingDataName, delimiter=',', usecols=[0])
	
	if test_flag == "ON":
		X_test = np.loadtxt(testingDataName, delimiter=',', dtype=dtype, usecols=[2,3,4,5,6,7])
		normalizeDataset(X_train, X_test) 
	else:
		normalizeDataset(X_train)

		
	X_train_part1,X_train_part2 = split_data(X_train)
	best_c,best_g = cross_validiation(X_train,X_train_part1,X_train_part2, Y_train, lambd,dtype)

	training_kernel = get_training_kernel(X_train, X_train_part1, X_train_part2, best_g, lambd, dtype)
	best_param_list = '-s 3 -t 4 -q -c '+str(best_c)
	best_svm_param = svm_parameter(best_param_list)
	prob = svm_problem(Y_train, training_kernel, isKernel=True)
	best_svm_model = svm_train(prob, best_svm_param)

	if test_flag == "ON":
		Y_test = np.loadtxt(testingDataName, delimiter=',', usecols=[0])
		Y_hat, p_acc = svm_prediction(X_train,X_test,best_svm_model,best_g,lambd,dtype,Y_test)
		#print("testing takes time: "+str(time.clock() - start_time))

		benchmark = sum(Y_test)+sum(Y_train)
		total = sum(Y_hat)+sum(Y_train)
		APD = abs(total-benchmark)
		RPD = APD/benchmark
		MAD = sum(abs(Y_test-Y_hat))/100000
		RMSE = np.sqrt(sum((Y_test-Y_hat)**2)/100000)
		# output = np.array([APD,RPD,MAD,RMSE])
		# np.savetxt(folder+"/svr_random_results.csv", output.reshape(1, output.shape[0]),fmt="%12.5f",delimiter=",")



if __name__ == "__main__":
	import timeit
	print(timeit.timeit("main()", setup="from __main__ import main",number=1))
