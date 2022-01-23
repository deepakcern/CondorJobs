#!/bin/sh
#### FRAMEWORK SANDBOX SETUP ####
# Load cmssw_setup function
export SCRAM_ARCH=slc7_amd64_gcc630
source ./cmssw_setup.sh

# Setup CMSSW Base
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

# Setup framework from sandbox
cmssw_setup sandbox-CMSSW_9_3_8-668d718.tar.bz2 


cd $CMSSW_BASE
cmsenv
cd ../../
tar xzvf ExRootAnalysis_V1.1.5.tar.gz 
cd ExRootAnalysis
make

NEvents=10000
RandomSeed=1234
NumberOfCPUs=4
path="/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.0/monoHiggs/2HDMa/"
gridpackName="$1" 
outputFileName="$2"
cp $path$gridpackName .

echo "cheking contents in the current directory"
ls 
echo "extracting gridpack "
tar -xavf $gridpackName
echo "running shell script to produce LHE file"
./runcmsgrid.sh $NEvents $RandomSeed $NumberOfCPUs

echo "LHE production file is done "
ls

echo "converting LHE file into root"
./ExRootLHEFConverter cmsgrid_final.lhe $outputFileName 

echo "All processes are done now"


if [ -e "$2" ]; then
    #until xrdcp -f "$2" root://eoscms.cern.ch//eos/cms/store/group/phys_exotica/monoHiggs/monoHbb/LHEFiles/"$2"; do
    until xrdcp -f "$4" root://se01.indiacms.res.in:1094//dpm/indiacms.res.in/home/cms/store/user/dekumar/t3store2/Signal_LHEFiles_2hdma/"$2"; do
    sleep 60
    echo "Retrying"
  done

fi

exitcode=$?

if [ ! -e "$2" ]; then
  echo "Error: The python script failed, could not create the output file."
  
fi
exit $exitcode
