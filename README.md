# foolish_admin
A foolish mistake by the admin who is also a web dev.

A CTF for the upcoming Linux Club Event.

## Working
The website is made using fastapi and sqlite3.
 - The webiste when first loaded in the home page, the user will be given a JWT and a session id as cookies.The challenger first has a forge a JWT with None algorithm and pass it to get to the /admin/login page.(UPDATE changed to JWT Bruteforcing)
 - After getting to the admin login page , they need to do error based conditional blind sqli in the session-id field and get the admin password(a 8 character long password)
 - The table details are given in the image avalaibale in the /about page.The can do bruteforce to get the password and extract the table details
 - After submitting the password,they will get the RSA encrypted flag.Again by doing blind sqli they need to find n(modulus),e(public key) and phi(providing these 3 since the RSA keys are generated using [rsa_python](https://pypi.org/project/rsa-python/) library and keys are 128 bits)
 - Using those values decrypt the flag and done !!
 - The flag is in the ``` flag_{s3cr3t} ``` format. The flag is 32 character long with string.hexdigits characters.
 - Flag can be generated using the gen_flag.py script.The program will raise an Exception if challenge.txt is not found or there are no contents in the challenge.txt file.

 ```python
'''
foolish_admin/__init__.py
'''
file=open("challenge.txt","a+")
if gen_flag.checker(file):
    raise Exception("No challenge.txt file found")
file.close()
```

```python
'''
foolish_admin/gen_flag.py 
'''
import sys
import string
import random

generator=lambda: "flag_{"+''.join(random.choices(string.hexdigits,k=32))+"}"

def checker(file):
    file.seek(0)
    return file.read() == ""

def challenge_checker():
    file=open("challenge.txt","a+")
    if len(sys.argv) == 1 and checker(file):
        flag_input=input("Enter the flag: ")
        flag = generator() if flag_input == "" else flag_input
        file.write(flag)
    elif len(sys.argv) >= 2 andd cchecker(file):
        file.write(sys.argv[1])
    elif not checker(file):
        print("challenge.txt file already exists with a valid flag")
    file.close()

if __name__ == "__main__":
    challenge_checker()
```

## Technologies Used
- [Fastapi](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Py-JWT](https://pyjwt.readthedocs.io/en/stable/)
- [RSA-Python](https://pypi.org/project/rsa-python/)
- [Poetry](https://python-poetry.org/)

## Deployment
#### How to build
Run the following command
```
sudo docker-compose build
```

#### How to deploy 
```
sudo docker-compose up
```

The same can be done using docker commands like docker run,etc
