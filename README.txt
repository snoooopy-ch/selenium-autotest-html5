How to build

docker build --tag dataq .
docker run -i -t --name dataqcontainer dataq




usage: dataq.py [-h] [-r URL] [-u USER] [-p PASSWORD] [-s SCRIPTS] [-a]

optional arguments:
  -h,			--help			show this help message and exit
  -r URL,		--url URL		input site url, default 'http://dataq-automation-alb-1598668034.us-east-1.elb.amazonaws.com:7000'
  -u USER,		--user USER		input login user, default 'john'
  -p PASSWORD,		--password PASSWORD	input login pass, default 'dataq'
  -s SCRIPTS,		--scripts SCRIPTS	input script number to execute using comma
  -a,			--all			all scripts

example:
run TC001			python dataq.py -s 1
run TC001 and TC002		python dataq.py -s 1,2
run TC001, TC006~TC009		python dataq.py -s 1,6,7,8,9
run all				python dataq.py
run all				python dataq.py -all
chanage user			python dataq.py -u morimura -p password
change url			python dataq.py -r http://dataq.example.com
