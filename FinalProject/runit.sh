#!/bin/bash
# This file pulls in the dependencies required to run
# the analyses via the various methods. It should install
# anaconda on the user system and when commands are given
# Perform either doc2vec or LSI modelling on a preset
# test script
# __author__ = Andy Fabian

CONDA=conda/bin/conda
ACTIVATE=conda/bin/activate
PYTHON=/usr/bin/pythonxxx
BASEDIR=`pwd`

echo "Creating logs directory"

mkdir logs 2>/dev/null

echo "Checking build system"

dpkg -l | grep build-essential | grep ii > /dev/null
if [[ "$?" == "1" ]]; then
    echo "Please run the following commands, and then re-run this script:"
    echo "  sudo apt-get install build-essential"
    echo "  sudo apt-get install sl"
    exit 1
fi

echo "Checking for working Anaconda installation"

test -e $CONDA
if [[ "$?" == "1" ]]; then
    echo "Anaconda not found.  Installing to $BASEDIR/conda."
    rm -rf conda
    test -e Anaconda3-4.2.0-Linux-x86_64.sh
    if [[ "$?" == "1" ]]; then
        wget https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh
    fi
    chmod u+x Anaconda3-4.2.0-Linux-x86_64.sh
    ./Anaconda3-4.2.0-Linux-x86_64.sh -b -p $BASEDIR/conda
fi

echo "Removing existing Anaconda project environment (if it exists)"

rm -rf conda/envs/NLPEnvironment

echo "Setting up Anaconda project environment"

$CONDA env create -n NLPEnvironment -f conda-settings.yml
source $ACTIVATE NLPEnvironment

echo "The following packages are installed:"
$CONDA list

echo "Running NLTK Setup"
python setup.py

echo "Executing Competition Entry"
echo "Results will be in: $BASEDIR/FeatureDevelopment/output.pred"

rm -f $BASEDIR/FeatureDevelopment/output.pred

cd FeatureDevelopment
python Main.py
cd ..

echo "Checking for working Python 2.7 installation"

PYTHONVERSION=`$PYTHON --version 2>&1 | cut -c 1-10`
if [[ "$PYTHONVERSION" != "Python 2.7" ]]; then
    PYTHON=$BASEDIR/Python-2.7.12/python
PYTHONVERSION=`$PYTHON --version 2>&1 | cut -c 1-10`
fi
if [[ "$PYTHONVERSION" != "Python 2.7" ]]; then

    echo "Installing Python 2.7"

    test -e Python-2.7.12.tgz
    if [[ "$?" == "1" ]]; then
        wget https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tgz
    fi
    tar -zxvf Python-2.7.12.tgz
    pushd Python-2.7.12
    ./configure
    make -j8
    PYTHON=`pwd`/python
    popd
fi

echo "Using $PYTHON"

echo "Executing Scorer"

cd scorer
$PYTHON ./MAP_scripts/ev.py SemEval2016-Task3-CQA-QL-dev.xml.subtaskB.relevancy $BASEDIR/FeatureDevelopment/output.pred

cd ..

$PYTHON modelRunner.py $PYTHON
