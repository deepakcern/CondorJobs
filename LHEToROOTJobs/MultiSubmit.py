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

def submitjob(gridpack_name,outputname,gridpack_path):
    #global count
    submittemp=open("submit_multi_temp.sub","w")
    submitfile=open("submit_multi.sub","r")
    for line in submitfile:
        # if line.startswith('transfer_input_files'):
        #     submittemp.write(line.strip()+', '+txtfile+'\n')
        # else:
        submittemp.write(line)
    submitfile.close()
    dummy='dummy'
    submittemp.write("arguments = "+gridpack_name+" "+outputname+"  "+gridpack_path+'\nqueue')
    submittemp.close()


    print "\n===============================\nSubmitting jobs for #" + gridpack_name+"\n===============================\n"

    if not test: os.system("condor_submit submit_multi_temp.sub")

    #count+=1


if __name__== "__main__":
    test=False
    count=0

    for outdirs in ['error','log','output']:
	os.system("mkdir -p "+outdirs)

    fin = open("gridpacks_2hdma_ggF.txt") # pass txt file where  gridpack location written

for line in fin:
    gridpack_name = line.rstrip().split('/')[-1]
    gridpack_path = line.replace(gridpack_name, '')
    print 'gridpack_path',gridpack_path
    outputname    = gridpack_name.replace("_slc6_amd64_gcc630_CMSSW_9_3_8_tarball.tar.xz",'.root')
    submitjob(gridpack_name,outputname,gridpack_path)
    count+=1

print 'Total number of jobs: ',count
