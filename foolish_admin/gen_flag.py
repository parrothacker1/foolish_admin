#!/bin/python3

import sys
import string
import random

generator=lambda: "flag_{"+''.join(random.choices(string.hexdigits,k=32))+"}"

def checker(file) -> bool:
    file.seek(0)
    return file.read() == ""

def challenge_checker():
    file=open("challenge.txt","r+")
    if len(sys.argv) == 1:
        flag_input=input("Enter the flag text (Enter none for random characters string): ")
        flag = generator() if flag_input=="" else flag_input
        file.seek(0)
        file.write(flag)
    elif len(sys.argv) >= 2:
        file.write(sys.argv[1])
#    elif not checker(file):
#        print("challenge.txt file already exists with a valid flag")
    file.close()

if __name__=="__main__":
    challenge_checker()
