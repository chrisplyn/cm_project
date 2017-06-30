
FOR /L %%k IN (1 1 30)DO (
	FOR %%S IN (100 500 1000 2000) DO (		
 		python kriging.py CM_project\scenario_%%k\%%S > CM_project\scenario_%%k\%%S\kriging_random_time.txt
		))
pause