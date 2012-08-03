#!/bin/bash
python_version=`python -c 'import sys; print(sys.version[:3])'`
PROJECT='jomtest'
ENV=pyenv
virtualenv --no-site-packages $ENV
rm $PROJECT/python
ln -s ../$ENV/bin/python $PROJECT/python
source $ENV/bin/activate
pip install -r requirements.txt

