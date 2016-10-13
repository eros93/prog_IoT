#!/usr/bin/python

from calculator import Calculator

if __name__ == "__main__":
	my_calc_1 = Calculator("calculator_1");

ans=True
while ans:
    input_string=raw_input("\n\tInsert <command> <operator1> <operator2> ... <operatorN> :\n\t") 
    input_list = input_string.split(' ')
   # input_list = input_list.reverse()
    ans=input_list.pop(0)
    print ans
    op1=float(input_list[1])
    op2=float(input_list[2])

    if ans=="add": 
      print("\n ADDITION") 
      result = my_calc_1.add(op1,op2)
      print "\t%s: the result is %.2f \n" % (my_calc_1.getID(), result)

    elif ans=="sub":
      print("\n SUBSTRACTION") 
      result = my_calc_1.sub(op1,op2)
      print "\t%s: the result is %.2f \n" % (my_calc_1.getID(), result)

    elif ans=="mul":
      print("\n MULTIPLICATION") 
      result = my_calc_1.mul(op1,op2)
      print "\t%s: the result is %.2f \n" % (my_calc_1.getID(), result)

    elif ans=="div":
      print("\n DIVISION") 
      try:
      	result = my_calc_1.div(op1,op2)
      except ZeroDivisionError:
      	print "\tCan't divide by zero"
      else:
      	print "\t%s: the result is %.2f \n" % (my_calc_1.getID(), result)

    elif ans !="":
      print("\n\tNot Valid Choice Try again") 



	# result = my_calc_1.add()
	# print "%s: the result for the addition is %f" % (my_calc_1.getID(), result)

	# result = my_calc_1.add(3)
	# print "%s: the result for the addition is %.2f" % (my_calc_1.getID(), result)

	# result = my_calc_1.add(3, 4.457)
	# print "%s: the result for the addition is %.3f" % (my_calc_1.getID(), result)


	# print "---"
	# my_calc_2 = Calculator("I_am_different!!");
	# result = my_calc_2.add(12, 1.23)
	# print "%s: the result for the addition is %.2f" % (my_calc_2.getID(), result)



