import os
from glob import glob

files=glob('output/*')

count=0

FailedID = []
for file in files:
	f=open(file,'r')
        failedJob=True
	for line in f:
	    if "written" in line and '.root' in line:
#		print "failed job:   ", file
                #count+=1
                failedJob=False
         
		break
	    #else:continue
        if failedJob: 
	     print "failed job:   ", file
             count+=1
             FailedID.append(file.split('/')[-1].split('.')[1])


print "Total failed jobs:   ", count

#print "IDs", FailedID


path='.'
dirs=[ i for i in os.listdir(path) if 'tempFilelists' in i]
fnlDir=sorted(dirs)[-1]



files = []

logFile=open('logsubmit.txt','r')

lines=logFile.readlines()


jobIDs=[]
txtFiles=[]
for i, j in enumerate(lines):
    if 'cluster' in j:
	jobID = j.split()[-1].replace('.','')
        jobIDs.append(jobID)
        txtFiles.append(lines[i-4].split()[-1])#+'.txt')
        #print 'jobID', jobID, 'lines', lines[i-4]

os.system('rm -rf Filelists_failed') 
os.system('mkdir Filelists_failed')
#deadfile=open('removedeadFiles.sh','w')
print jobIDs
for i, j in enumerate(jobIDs):
    if j in FailedID:
	print txtFiles[i]
	os.system('cp '+txtFiles[i]+' '+'Filelists_failed')

        #deadfile.write('rm -rf'+' '+txtFiles[i].replace('.txt','.root')+'\n')
        #print 'failes job', j , 'files', txtFiles[i] 
