while(True):
    try:
        number1 = int(input("Enter first Number: "))
        number2 = int(input("Enter second NUmber: "))

        answer = number1/number2
        print(f"Answer is {answer}")
    except:
        print("Some Error Occurred......")