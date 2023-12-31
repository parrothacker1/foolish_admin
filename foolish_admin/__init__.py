from foolish_admin.main import app
from foolish_admin import gen_flag

file=open("challenge.txt","a+")
if gen_flag.checker(file):
    raise Exception("No challenge.txt file found")

file.close()
