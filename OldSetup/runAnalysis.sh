#!/bin/sh
#### FRAMEWORK SANDBOX SETUP ####
# Load cmssw_setup function
export SCRAM_ARCH=slc6_amd64_gcc700
source ./cmssw_setup.sh

# Setup CMSSW Base
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

# Download sandbox
#wget --no-check-certificate "http://stash.osgconnect.net/+ptiwari/sandbox-CMSSW_8_0_26_patch1-76efecd.tar.bz2"

# Setup framework from sandbox
cmssw_setup sandbox-CMSSW_10_3_0-4cef61e.tar.bz2

cd $CMSSW_BASE
cmsenv
cd ../../

python SkimTree.py -y 2017 -F -i "$1"

if [ -e "$4" ]; then
  until xrdcp -f "$4" root://eoscms.cern.ch//eos/cms/store/group/phys_exotica/bbMET/2017_skimmedFiles/V0/MC/"$4"; do 
    sleep 60
    echo "Retrying"
  done

fi

exitcode=$?

if [ ! -e "$4" ]; then
  echo "Error: The python script failed, could not create the output file."
  
fi
exit $exitcode

