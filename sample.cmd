
FOR /L %%k IN (1 1 30) DO (
	FOR %%S IN (100 500 1000 2000) DO (		
 		Rscript randomSampling.R %%k %%S
		))
pause