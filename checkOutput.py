import os
from glob import glob

files=glob('output/*')

count=0
for file in files:
	f=open(file,'r')
	for line in f:
	    if "The python script failed" in line:
		print "failed job:   ", file
                count+=1
		break
	    else:continue


print "Total failed jobs:   ", count
