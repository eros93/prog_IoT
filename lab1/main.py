#!/usr/bin/python

from calculator import Calculator
import json

if __name__ == "__main__":
	my_calc_1 = Calculator("calculator_1");

ans=True
print ("\n\n\t--------> PYTHON CALCULATOR PLUS <--------\n")
print ("\t------------> Powered by E&E <------------")
while ans:
    input_string=raw_input("\n\n\tInsert <command> <operator1> <operator2> ... <operatorN> :\n\t") 
    input_list = input_string.split(' ')
   # input_list = input_list.reverse()
    ans=input_list.pop(0)
    obj={}
    obj["command"] = ans
    op=[]
    n=len(input_list)
    for x in xrange(0,n):
    	op.insert(x,float(input_list.pop(0)))
    

    if ans=="add": 
      print("\n\t\tADDITION") 
      result=op.pop(0)
      obj["op1"] = result
      for x in xrange(0,n-1):
      	temp_str="op"+str(x+2)
      	temp_op = op.pop(0)
      	obj[temp_str]=temp_op
      	result=my_calc_1.add(result,temp_op)
      print "\n\t%s: the result is %.2f \n" % (my_calc_1.getID(), result)
      obj["result"] = result
      output_json=json.dumps(obj)
      print output_json


    elif ans=="sub":
      print("\n\t\tSUBSTRACTION") 
      result=op.pop(0)
      obj["op1"] = result
      for x in xrange(0,n-1):
      	temp_str="op"+str(x+2)
      	temp_op = op.pop(0)
      	obj[temp_str]=temp_op
      	result=my_calc_1.sub(result,temp_op)
      print "\n\t%s: the result is %.2f \n" % (my_calc_1.getID(), result)
      obj["result"] = result
      output_json=json.dumps(obj)
      print output_json


    elif ans=="mul":
      print("\n\t\tMULTIPLICATION") 
      result=op.pop(0)
      obj["op1"] = result
      for x in xrange(0,n-1):
      	temp_str="op"+str(x+2)
      	temp_op = op.pop(0)
      	obj[temp_str]=temp_op
      	result=my_calc_1.mul(result,temp_op)
      print "\n\t%s: the result is %.2f \n" % (my_calc_1.getID(), result)
      obj["result"] = result
      output_json=json.dumps(obj)
      print output_json


    elif ans=="div":
      print("\n\t\tDIVISION") 
      try:
      	result=op.pop(0)
      	obj["op1"] = result
      	for x in xrange(0,n-1):
      	  temp_str="op"+str(x+2)
      	  temp_op = op.pop(0)
      	  obj[temp_str]=temp_op
      	  result=my_calc_1.div(result,temp_op)
      except ZeroDivisionError:
      	print "\t\nCan't divide by zero"
      else:
      	print "\t\n%s: the result is %.2f \n" % (my_calc_1.getID(), result)
      obj["result"] = result
      output_json=json.dumps(obj)
      print output_json


    elif ans !="":
      print("\n\tNot Valid Choice Try again")