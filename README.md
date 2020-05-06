## Create project directory:
> mkdir academic_data
> cd academic_data

## Install virtual env
> sudo apt-get install python3-pip
> sudo pip3 install --upgrade virtualenv

## Create Virtual env
> virtualenv -p python3 venv

## Activate virtualenv
> source venv/bin/activate

## paste the all the contents of zip file here, like below
> ls academic_data/
config.py
README.md
requirements.txt
app.py

## Install requirements
> pip3 install < requirements.txt

## Run python file
> python3 app.py

## Hit Api on browser to extract academic staff details
http://localhost:5000/get/academic/data

## one excel file will get created in academic_data directory/folder which contains information.