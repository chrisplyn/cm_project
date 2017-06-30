import numpy as np

def output(method, stat_name, value):

	if stat_name == "mean":
		output = open(method+"_scenario_mean.csv", "w")
	elif stat_name == "std":
		output = open(method+"_scenario_std.csv", "w")
	else:
		output = open(method+"_scenario_cv.csv", "w")
	
	header = "k,APD,RPD,MAD,RMSE"	
	output.write(header)
	output.write("\n")
	
	for i in range(4):
		if i == 0:
			output.write("100,")
		elif i == 1:
			output.write("500,")
		elif i == 2:
			output.write("1000,")
		else:
			output.write("2000,")

		for j in range(4):		
			mean = np.mean(value[i,j])
			std = np.std(value[i,j])
			cv = std/mean

			if stat_name == "mean":
				output.write(str(mean)+",")		
			elif stat_name == "std":
				output.write(str(std)+",")
			else:
				output.write(str(cv)+",")

		output.write("\n")	
	output.close()


def summary(method_name):
	result_table = np.zeros((4, 4, 30))

	for no in range(1, 31):
		for k in (100, 500, 1000, 2000):
			if method_name  == "bt_random":
				filePath = "CM_project/scenario_"+str(no)+"/"+str(k)+"/bt_random_results.csv"
				value_table = np.loadtxt(filePath, delimiter=',')
			elif method_name == "svr_random":
				filePath = "CM_project/scenario_"+str(no)+"/"+str(k)+"/svr_random_results.csv"
				try:
					value_table = np.loadtxt(filePath, delimiter=',')
				except:
					print(str(no)+","+str(k))				
			else:
				filePath = "CM_project/scenario_"+str(no)+"/"+str(k)+"/kriging_random_results.csv"
				value_table = np.loadtxt(filePath, delimiter=',')
		
			for j in range(4):
				# if j == 2:
				# 	value_table[j] = np.sqrt(value_table[j])

				if k == 100:
					result_table[0,j,no-1] = value_table[j]
				elif k == 500:
					result_table[1,j,no-1] = value_table[j]
				elif k == 1000:
					result_table[2,j,no-1] = value_table[j]
				else:
					result_table[3,j,no-1] = value_table[j]
	return result_table			



def running_time(filename):
	time_table = np.zeros((4, 30))

	for no in range(1, 31):
		for k in (100, 500, 1000, 2000):
			filePath = "CM_project/scenario_"+str(no)+"/"+str(k)+"/"+filename
			time = np.loadtxt(filePath)
			
			if k == 100:
				time_table[0,no-1] = time
			elif k == 500:
				time_table[1,no-1] = time
			elif k == 1000:
				time_table[2,no-1] = time
			else:
				time_table[3,no-1] = time
	output=""			
	for j in range(4):
		output += " "+str(np.mean(time_table[j]))
	print(output)


def main():
	value = summary("kriging_random")
	method = "kriging_random"
	output(method, "mean", value)
	output(method, "std", value)
	output(method, "cv", value)
	# running_time("kriging_time.txt")


if __name__ == "__main__":
	main()
