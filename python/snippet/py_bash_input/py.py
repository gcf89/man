#!/usr/bin/env python

#import subprocess
#
#output
#try:
#	res = subprocess.check_output("bash input.sh < data", stderr=subprocess.STDOUT, shell=True)
#	print res
#except subprocess.CalledProcessError:
#	print "Process exit code != 0"

from subprocess import Popen, PIPE, STDOUT
#import multiprocessing
from multiprocessing import Pool, TimeoutError, Process, Lock, Array, Value, Manager
from ctypes import c_char_p
#import time
#import os


def run_cmd(cmd):
	proc = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
	proc.wait()
	stdout, stderr = proc.communicate()
	return proc.returncode, stdout, stderr


def run_cmd2(cmd):
	proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
	proc.wait()
	stdout, stderr = proc.communicate()
	return proc.returncode, stdout

def run_cmd_mp(cmd, output):
	#print cmd
	proc = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
	proc.wait()
	stdout, stderr = proc.communicate()
	output.value = stdout


def test_run_cmd():
	rt, out, err = run_cmd("bash input.sh < data")
	
	print 'retcod:', rt
	print 'stdout:', out
	print 'stderr:', err
	
	rt, out = run_cmd2("bash input.sh < data")
	
	print 'retcod:', rt
	print 'stdout:', out


def cmd_callback(output):
	'''
	callback func for test in Pool.apply_async call
	'''
	print 'cmd_callback:', output



if __name__ == '__main__':
	#pool = Pool(processes=multiprocessing.cpu_count())
	#multiple_results = [pool.apply_async(run_cmd, "bash input.sh < data") for i in range(8)]
	#print [res.get(timeout=10) for res in multiple_results]
	#multiple_results = pool.apply_async(run_cmd, "bash input.sh < data")
	#print multiple_results.get(timeout=10)

	manager = Manager()
	#string = manager.Value(c_char_p, "String")
	#ind = Value('i', 0)
	#res = Value('c_char_p', "D")
	#arr = Array('c_char_p', 1)
	#p = Process(target=run_cmd_mp, args=(("bash input.sh < data"), ind, string))
	#p.start()
	#p.join()
	#print list(arr)
	#print string.value

	
	l = [
		"bash input.sh < data",
		"bash input.sh < data",
		"bash input.sh < data",
		"bash input.sh < data",
		"bash input.sh < data",
	]

	d3 = {}
	for i in range(5):
		d3[i] = manager.Value(c_char_p, "String")
	
	for i, cmd in enumerate(l):
		p = Process(target=run_cmd_mp, args=(cmd, d3[i]))
		p.start()
		p.join()

	for key, output in d3.iteritems():
		print output.value


