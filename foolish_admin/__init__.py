from foolish_admin.main import app

import random
import string

file=open("challenge.txt","a+")
challenge_txt="flag_{"+''.join(random.choices(string.hexdigits,k=32))+"}"
if file.read() == '':
    file.write(challenge_txt)

file.close()
