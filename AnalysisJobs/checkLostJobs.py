import os

from glob import glob

logFile=open('logsubmit.txt','r')

lines=logFile.readlines()

testCount =0
txtFiles = []
jobIDs=[]
txtFiles=[]
FailedClusterTxt =[]
for i, j in enumerate(lines):
    if 'cluster' in j:
        jobID = j.split()[-1].replace('.','')
        jobIDs.append(jobID)
        txtFiles.append(lines[i-4].split()[-1])
    if "Filelists" in j and not 'cluster' in lines[i+4]:
	testCount = testCount +1
	FailedClusterTxt.append(j.split()[-1])
	print " Failed txt file to be submitted : ", j.split()[-1] 
	print '',lines[i+4]
#condor.10575591.0.out
outputs = glob('output/*out')
ClusterIDs = [ID.split('/')[-1].replace('.0.out','').replace('condor.','') for ID in outputs]
#print "testCount",testCount
print "txtFiles",len(txtFiles)
print "jobIDs ",len(jobIDs),jobIDs[0]
print "ClusterIDs ",len(ClusterIDs),ClusterIDs[0]

jobIDs =set(jobIDs)
ClusterIDs =set(ClusterIDs)

lostIDs =jobIDs-ClusterIDs
'''
for jobID in jobIDs:
    isFaledJob = False
    for tesID in ClusterIDs:
	if jobID==tesID: isFaledJob=True
    if isFaledJob:lostIDs.append(jobID)

'''

print "lostIDs  ",len(lostIDs),lostIDs
