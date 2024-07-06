# namelistgenerator.py
Generates a name list of active directory users.

Given a list of employees full name like:
John Moris
Steven Brook

the script will generate name lists in different username formats commonly seen in active directory environments.
Eg. jmoris, morisj, john.moris, john


## Usage
python3 namelistgenerator.py -c companyname -f employeelist.txt