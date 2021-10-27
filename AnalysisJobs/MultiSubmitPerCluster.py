from itertools import izip_longest
import os,sys,datetime
from glob import glob


def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def splitTxt(txtfile,dirName,maxFilePerTxt):
    n=maxFilePerTxt
    with open(txtfile) as f:
        newtxt=txtfile.split('/')[-1].replace('.txt','')
        for i, g in enumerate(grouper(n, f, fillvalue=''), 1):
            with open(dirName+'/'+newtxt+'_{0}.txt'.format(i), 'w') as fout:
                fout.writelines(g)

def submitjob(inFiles,dirName):
    #global count
    submittemp=open("submit_multi_temp.sub","w")
    submitfile=open("submit_multi.sub","r")
    for line in submitfile:
        if line.startswith('transfer_input_files'):
            submittemp.write(line.strip()+', '+dirName+'\n')
        else:
            submittemp.write(line)
    submitfile.close()
    dummy='dummy'
    for txtfile in inFiles:
	print "\n===============================\nSubmitting jobs #"+str(count)+": "+ txtfile+"\n===============================\n"
    	submittemp.write("arguments = "+dirName+"/"+txtfile.split('/')[-1]+" "+dummy+" "+dummy+"  "+"Analysis_"+txtfile.split('/')[-1].replace('.txt','.root ')+'  $(Proxy_path)'+'\nqueue'+'\n')
    submittemp.close()


    #print "\n===============================\nSubmitting jobs #"+str(count)+": "+ txtfile+"\n===============================\n"

    if not test: os.system("condor_submit submit_multi_temp.sub")

    #count+=1


if __name__== "__main__":
    test=False
    count=0
    FilesToSubmit ='Filelists_v12.07_NLO_Samples_uscms_pt18_data'#'Filelists_v12.07_NLO_Samples_uscms_pt18_DYJets'#'Filelists_v12.07_test'#'Filelist_skim_v17_08-00-00_DATA'#'Filelists_v12.07_NLO_Samples_uscms_pt18_all'#'Filelist_skim_v17_08-00-00_DATA'#'Filelists_v12.07_NLO_Samples_uscms_pt18_all'#'Filelists_v12.07_NLO_Samples_uscms_pt18_Z2Jets'#'Filelist_skim_v17_08-00-00_DATA'#'Filelists_v12.07_ALL'#'Filelists_setup_2017_NLOSamples'#'Filelist_setup_2017_v17_07_missing'#'Filelists_v06_all'
    FilesToResubmit = "Filelists_failed"

    if not test: os.system("chmod +x runAnalysis.sh")
    for outdirs in ['error','log','output']:
        os.system("mkdir -p "+outdirs)

    IsSkimJobs =False;submitJob=False;ResubmitJob=False
    if sys.argv[1]=="skim":
	IsSkimJobs=True
    if sys.argv[2]=="submit":
        submitJob=True
    elif sys.argv[2]=="resubmit":
        ResubmitJob=True
    else:
        print "Please provide correct arguments, check the code for usage+\n"
        sys.exit()

    maxfilesperjob=5
    if IsSkimJobs and not ResubmitJob: # This part is to submit skim jobs with multiple root file per job
        listfiles = [f for f in os.listdir(FilesToSubmit) if f.endswith('.txt')]
        dirName='tempFilelists_'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	os.system("mkdir -p "+dirName)
	for txtfile in listfiles:
	    splitTxt(FilesToSubmit+'/'+txtfile,dirName,maxfilesperjob)
    elif ResubmitJob: 
	#This part is to resubmit failed skim jobs, provide same input txt files which are failed,
	#copy those input txt files from tempFilelists* directory
	dirName=FilesToResubmit
    elif not IsSkimJobs: # this part is for analyser job: job with single root file. Each txt file is with single root file
	dirName=FilesToSubmit
    MytxtFiles = [f for f in os.listdir(dirName) if f.endswith('.txt')]


    nJobsPerCluster = 1
    setOfFiles = [MytxtFiles[i * nJobsPerCluster:(i + 1) * nJobsPerCluster] for i in range((len(MytxtFiles) + nJobsPerCluster - 1) // nJobsPerCluster )]
    #print setOfFiles
    for ij in range(len(setOfFiles)):
	inFiles =setOfFiles[ij]
	submitjob(inFiles,dirName)
	count = count + len(inFiles)

'''
for ifile in MytxtFiles:
    submitjob(count,dirName+'/'+ifile)
    count+=1
'''
print 'Total number of jobs: ',count
