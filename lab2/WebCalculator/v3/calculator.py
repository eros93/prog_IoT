#!/usr/bin/python

import json
import cherrypy

class WebCalculatorV2(object):

	exposed=True

	def __init__(self, id):
		self.id = id

	def add (self, operator1=0, operator2=0):
		return operator1 + operator2

	def sub (self, operator1=0, operator2=0):
		return operator1 - operator2

	def mul (self, operator1=0, operator2=0):
		return operator1 * operator2

	def div (self, operator1=0, operator2=0):
		return operator1 / operator2

	def getID (self):
		return self.id

	def calculate(self):
		if self.command == "add": 
			print("\nADDITION")
			return (self.add(self.operator1,self.operator2))

		elif self.command == "sub": 
			print("\nSUBSTRACTION")
			return (self.sub(self.operator1,self.operator2))

		elif self.command == "mul": 
			print("\n\MULTIPLICATION")
			return (self.mul(self.operator1,self.operator2))

		elif self.command == "div": 
			print("\n\DIVISION")
			try:
				result = self.div(self.operator1,self.operator2)
			except ZeroDivisionError:
				print "\n\tCan't divide by zero"
			else:
				return result


	def GET (self, *uri, **params):
		self.command = uri[0]

		if len(uri)!=3:
			return "You are missing at least one parameter! <br/><br/>Remember:	./'command'/'operator1'/'operator2'"

		try:
			self.operator1 = float(uri[1])
		except ValueError:
			return "Operator1 is not a number! Try again"
		
		try:
			self.operator2 = float(uri[2])
		except ValueError:
			return "Operator2 is not a number! Try again"

		if self.command == "div":
			if self.operator2 == 0:
				return "\n\tCan't divide by zero"

		if ((self.command!="add") and (self.command!="sub") and (self.command!="mul") and (self.command!="div")):
			return "\n\tNot Valid Command Try again"

		result = self.calculate()
		cherrypy.session['result'] = result

		params["op1"] = self.operator1
		params["op2"] = self.operator2
		params["command"] = self.command
		params["result"] = result
		output_json = json.dumps(params)
		
		return output_json	


	def POST(self, *uri, **params):
		json_input = cherrypy.request.body.read()
		input_list = json.loads(json_input)
		self.command = input_list["command"]
		n=len(input_list["operands"])
		op=input_list["operands"]

		if ((self.command!="add") and (self.command!="sub") and (self.command!="mul") and (self.command!="div")):
			return "\n\tNot Valid Command Try again"

		if self.command=="add": 
			result=float(op.pop(0))
			for x in xrange(0,n-1):
				temp_op = float(op.pop(0))
				result=self.add(result,temp_op)
			input_list = json.loads(json_input)
			input_list["result"] = result
			output_json=json.dumps(input_list)
			return output_json

		elif self.command=="sub": 
			result=float(op.pop(0))
			for x in xrange(0,n-1):
				temp_op = float(op.pop(0))
				result=self.sub(result,temp_op)
			input_list = json.loads(json_input)
			input_list["result"] = result
			output_json=json.dumps(input_list)
			return output_json

		elif self.command=="mul": 
			result=float(op.pop(0))
			for x in xrange(0,n-1):
				temp_op = float(op.pop(0))
				result=self.mul(result,temp_op)
			input_list = json.loads(json_input)
			input_list["result"] = result
			output_json=json.dumps(input_list)
			return output_json

		elif self.command=="div": 
			try:
				result=float(op.pop(0))
				for x in xrange(0,n-1):
					temp_op = float(op.pop(0))
					result=self.div(result,temp_op)
			except ZeroDivisionError:
				return "\n\tCan't divide by zero"
			else:	
				input_list = json.loads(json_input)
				input_list["result"] = result
				output_json=json.dumps(input_list)
				return output_json

