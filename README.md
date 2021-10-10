# trufla-coding-challenge



install python , python3.
using the folloing commands:(provide the password when prompted)


# ~$ sudo apt-get install python

  ~$ sudo apt-get install python3
------------------------------------------------------------------------
(OPTIONAL)(i would recommend installing conda evnviroment)
see this url for steps of installation.
url : https://docs.anaconda.com/anaconda/install/linux/
-------------------------------------------------------------------------------------------------------------------------
(OPTIONAL BUT RECOMMENDED)
after cloning the project i would recommend running this tool , just to fix any indentation errors(if you face any just run the command):
install autopep 8:

# ~$ pip install autopep8
 
 ~$ autopep8 -i parser.py
-------------------------------------------------------------------------------------------------------------------------
install requiremnts using the following command using the requirements.txt file and pip:
pip install -r /path/to/requirements.txt

or install them manually using the following commands:

# ~$ pip install typer

# ~$ pip install pandas

feature 3:

# ~$ pip install pymongo

-------------------------------------------------------------------------------------------------------------------------------
feature 1 and 2.
installation:
make sure the following line is the first line of the code.
#!/usr/bin/python3

to install as command run the following commands:

 Step 1: cd to project folder
# ~$ cd /path/to/script

for example : cd /home/fares/Desktop/trufla

 Step2:make the script executable:
 
# ~$ chmod +x <scriptname>.py

for example :chmod +x hello.py


Now you can run your python file like ./hello.py

 Step 3 : Move your file to bin to run it from anywhere
In terminal type the following command:

~$ which python3

it will return the path of python3
example:/usr/bin/python3


cp filename.py /usr/bin/python3/new_name_you want_to_run_with
For example I want to run this file by calling parser.py, I will do

~$ cp parser.py /usr/bin/python3/parser.py

Now you can run this welcome from anywhere on your system by just typing parser.py plus arguments in the terminal
example : parser.py xml file1
--------------------------------------------------------------------------------------------------------------------------------
feature 3.

install mongodb.

(installation guide)
see the following url :https://docs.mongodb.com/manual/installation/

select the proper installation guide for your own OS.

install mongodb compass or robo3t.
these are gui tools for managing mongodb.

connect to your local database.

open your mongod .
type: mongod

open your mongo shell. and type " use admin "
expected output is : switched db to admin
then type :

db.createUser(
  {
    user: "trufla_admin",
    pwd: "p@ssw0rd",
    roles: [
      { role: "userAdminAnyDatabase", db: "admin" },
      { role: "readWriteAnyDatabase", db: "admin" }
    ]
  }
)

now close your mongod and open it again with
~$ mongod --auth

connect to your database through mongodb compass

run the code
and refresh and check data.

-----------------------------------------------------------------------------------------------------------------------------

running steps:
p.s : make sure you have the input data files in the correct path
to run the script simply type "parser.py" choose from (xml or csv) filename. parser.py --help
step 1 :
type the script name
step 2 :
type the option or argument csv or xml

step 3 :
type the source input file(s)
for example:
parser.py xml <filename>
~$ parser.py xml file1

parser.py csv <customers_file> <vehicles_file>.
~$ parser.py csv customers vehicles

p.s:as csv are read from two files.all file names are typed without the extension

note : in feature one you only need to provide the filename as its the only option there.

--------------------------------------------------------------------------------------------------------------------------------------
check the output files and database.

