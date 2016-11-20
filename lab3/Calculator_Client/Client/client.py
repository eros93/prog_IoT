#!/usr/bin/python

import json
import requests
import string

if __name__ == "__main__":
	flag=True
	print ("\n\n\t--------> PYTHON CALCULATOR CLIENT <--------")
	print ("\n\t--------------> Powered by E&E <----------------")
	while flag:
		ready=False
		ans=string.lower(raw_input("\n\n\tOperation: "))

		if (ans=="add")|(ans=="addition"):
			ans="add"
			print("\n\n\tADDITION")
			op1=raw_input("\n\tInsert operator 1: ")
			op2=raw_input("\n\tInsert operator 2: ")
			if (op1.isdigit()==True)&(op2.isdigit()==True):
				op1=float(op1)
				op2=float(op2)
				ready=True
			else: print "\n\tOperator 1 or 2 is/are not correct!"

		elif (ans=="sub")|(ans=="substraction"):
			ans="sub"
			print("\n\n\tSUBSTRACTION")
			op1=raw_input("\n\tInsert operator 1: ")
			op2=raw_input("\n\tInsert operator 2: ")
			if (op1.isdigit()==True)&(op2.isdigit()==True):
				op1=float(op1)
				op2=float(op2)
				ready=True
			else: print "\n\tOperator 1 or 2 is/are not correct!"

		elif (ans=="mul")|(ans=="multiplication"):
			ans="mul"
			print("\n\n\tMULTIPLICATION")
			op1=raw_input("\n\tInsert operator 1: ")
			op2=raw_input("\n\tInsert operator 2: ")
			if (op1.isdigit()==True)&(op2.isdigit()==True):
				op1=float(op1)
				op2=float(op2)
				ready=True
			else: print "\n\tOperator 1 or 2 is/are not correct!"

		elif (ans=="div")|(ans=="division"):
			ans="div"
			print("\n\n\tDIVISION")
			op1=raw_input("\n\tInsert operator 1: ")
			op2=raw_input("\n\tInsert operator 2: ")
			if (op1.isdigit()==True)&(op2.isdigit()==True):
				op1=float(op1)
				op2=float(op2)
				if op2==0:
					print("\n\t--> Can't divide by 0! Try again...")
				else: ready=True
			else: print "\n\t--> Operator 1 or 2 is/are not correct!"
		
		elif (ans=="quit")|(ans=="end")|(ans=="stop"):
			print ("\n\t--> Exiting from PYTHON CALCULATOR PLUS ...\n\n")
			flag=False
		
		elif ans !="":
			print("\n\t--> Not Valid Choice Try again...")

		if ready==True:
			url_req='http://localhost:8080/'+ans
			parameters={'op1':op1, 'op2':op2}
			print("\n\tContacting CALCULATOR web service...")
			r=requests.get(url_req, params=parameters)
			if r.status_code==200:
				payload=json.loads(r.text)
				print("\t--> REQUEST SUCCESS!")
				print "\n\tResult: %f" %payload["result"]
			else: print("\n\tBad Response from Web Server")