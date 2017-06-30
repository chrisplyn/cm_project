
FOR /L %%k IN (1 1 30) DO (
	FOR %%S IN (100 500 1000 2000) DO (		
 		Rscript boosted_tree.R CM_project\scenario_%%k\%%S > CM_project\scenario_%%k\%%S\bt_random_time.txt
		))
pause