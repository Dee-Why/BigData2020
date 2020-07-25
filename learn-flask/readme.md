# learn-flask
learn how to use flask and make an  app to implement some AI tech.

## how to use
On windows (which is my case), things are a little sophiscated

* switch to the conda environment which has *flask* installed
* cd into the this folder
* type the following three commands
```shell script
set FLASK_APP=hello.py    # the app is written in hello.py
$env:FLASK_APP = "hello.py"   # note that the  '$' is a must
python -m flask run   # terminal output will tell where to go
```
then you can simply paste the output into your browser