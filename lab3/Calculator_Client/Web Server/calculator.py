#!/usr/bin/python

import json
import cherrypy

class WebCalculator(object):

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
			print("\nMULTIPLICATION")
			return (self.mul(self.operator1,self.operator2))

		elif self.command == "div": 
			print("\nDIVISION")
			try:
				result = self.div(self.operator1,self.operator2)
			except ZeroDivisionError:
				print "\n\tCan't divide by zero"
			else:
				return result


	def GET (self, *uri, **params):
		self.command = uri[0]

		if len(params.values())!=2:
			return "You are missing at least one parameter! <br/><br/>Remember:	./'command'?op1='operator1'&op2='operator1'"

		try:
			self.operator1 = float(params["op1"])
		except ValueError:
			return "Operator1 is not a number! Try again"
		
		try:
			self.operator2 = float(params["op2"])
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