
FOR /L %%k IN (2 1 30) DO (
	FOR %%S IN (100 500 1000 2000) DO (		
 		python svm_model.py CM_project\scenario_%%k\%%S ON > CM_project\scenario_%%k\%%S\svr_random_time.txt
		))
pause