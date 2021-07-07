from numbers_class import Number
import time

print("Application: Numbers - find out everything about a number")
print("Author: Stanislaw Rajm\n")
time.sleep(5)


n = input("Type in the number: ")
number = Number()
data = number.run(n)

if data:
    for k, v in data.items():
        if v:
            print("{0}: {1}".format(k, v))

print("")
input("Press enter to exit")
