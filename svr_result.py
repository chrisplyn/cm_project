#!/usr/bin/env python

import numpy as np
from sys import argv, exit


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def main():
	if len(argv) != 2:
		print("input folder")
		exit(1)	

	folder = argv[1]	
	tmp = open(folder +"/svr_result","r")	
	out = open(folder+"/svr_results","w")
	k = 0

	for line in tmp:
		if k==0 :
			k = k+1
			continue
		pos = find_nth(line,'.',4)
		new = line[:pos] + ',' + line[(pos+1):]
		out.write(new)

	tmp.close()
	out.close()


if __name__ == "__main__":
	main()
