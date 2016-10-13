#!/usr/bin/python

from calculator import Calculator

if __name__ == "__main__":
	my_calc_1 = Calculator("calculator_1");







ans=True
while ans:
    print ("""
    1.Addition
    2.Substraction
    3.Multiplication
    4.Division
    5.Exit
    """)
    ans=raw_input("Which operation do you need? ") 
    if ans=="1": 
      print("\n ADDITION") 
      op1=input("operator 1: ")
      op2=input("operator 2: ")
      result = my_calc_1.add(op1,op2)
      print "%s: the result is %.2f \n" % (my_calc_1.getID(), result)

    elif ans=="2":
      print("\n SUBSTRACTION") 
      op1=input("operator 1: ")
      op2=input("operator 2: ")
      result = my_calc_1.sub(op1,op2)
      print "%s: the result is %.2f \n" % (my_calc_1.getID(), result)

    elif ans=="3":
      print("\n MULTIPLICATION") 
      op1=input("operator 1: ")
      op2=input("operator 2: ")
      result = my_calc_1.mul(op1,op2)
      print "%s: the result is %.2f \n" % (my_calc_1.getID(), result)

    elif ans=="4":
      print("\n DIVISION") 
      op1=input("operator 1: ")
      op2=input("operator 2: ")
      result = my_calc_1.div(op1,op2)
      print "%s: the result is %.2f \n" % (my_calc_1.getID(), result)

    elif ans !="":
      print("\n Not Valid Choice Try again") 















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



