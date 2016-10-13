#!/usr/bin/python

class Calculator():

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
