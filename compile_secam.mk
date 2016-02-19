all:
	echo 'please specify a compiler!'
cython:
	cython --embed -o secam.c secam.py
	gcc -Os -I /usr/include/python2.7/ -o secam secam.c -lpython2.7 -lpthread -lm -lutil -ldl

nuitka:
	nuitka --recurse-directory=./ --recurse-directory=./path_crawler_helpers/  --recurse-directory=./examples/heater/ ./secam.py
