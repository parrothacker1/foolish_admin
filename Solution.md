# Solution For the CTF

The solution is pretty quite simple if you look into the problem.So the [Tux in space image](https://github.com/parrothacker1/foolish_admin/blob/main/foolish_admin/static/tuux_space.jpeg) has some steganographically hidden data.All you had to do was run a bruteforce on the steganography password.Now I don't know about tools that you can use, but it can be done easily with a simple py/bash script.(The password is a 3 letter word.A wild guess would also do). Now after getting all the necessary data you need, you can see the details about the admin(foolish guy who created the website) in the /about page.Keep thilh91s page in mind, we need this guys details later. Now if you have checked the cookies of the website, you can see that website stores the jwt and a session id.Now if you noted this during the challenge, I am sure that you analysed the jwt in the [jwt.io](https://jwt.io/), you can see that the payload has 2 keys and values role and isAdmin. I hope after reading till now you remember about the /about page.The admin details ... we can use that details to generate a wordlist.Now there are a lot of tools you can find in the industry but my personel favorite is the [cupp](https://github.com/Mebus/cupp) tool.You can use that wordlist to crack the jwt secret key. Now again for me personally a python script will work out to bruteforce.We can use [Py-JWT](https://pyjwt.readthedocs.io/) library to decrypt it (using the wordlist) and then sign it with a new payload with values of role as admin and isAdmin as true.Use it to get the access of the login page.After getting access to the login page.
Now that was a lot of steps.Yes I also agree to that but at I would also like to ask was any of these steps hard ? No right .. well you might say about the jwt part but if you know about jwts and it's working, this is a easy step. After this comes the real part .
Now here the data you extracted from the tux is gonna help you. You know about the columns nd the tables that are in the database from the tables.txt(from tux). Now we have all the data we need to do a blind sql injection.And here's another trouble.We don't know what database the admin is using and we cannot check it directly because we cannot see the output of our sql injection.

So here's another thing we can try.You know that the admin is a foolish guy.So like him the db might be foolish too (jk).Well what I said can also be true.So if you have tried any dbms,you know that it's not possible to do division by zero in any of the databases except for one,the SQLite.If you try division by zero in sqlite it will not return an error instead returns a int value.How about we try that on our database.If you try it , you will find out that the server doesn't return any errors.Now this confirms that our admin is not using mysql,postgres or any other like that since these will return error for sure.Now to confirm that the database is sqlite based, let's run another known error which qill trigger an error in sqlite3 the load_extension one.If you run it on sqlite without giving a valid path, it will return an error.And after trying it you can see that it returns a 500 response

Now we confirmed our database is sqlite3 and it is vulnerable to sql injection.Just pass the malicious code in the cookies using burpsuite(everything above mentioned can be done using burpsuite) and figure out the admin password.The code will look like this
```sql
xxxx' UNION SELECT 1,CASE(1=1) THEN 'a' ELSE load_extension(1) DONE --
```
Now why did I add one there is because UNION needs same column number and needs to be of same data type when using UNION.You can learn more about this on portswigger.net or learn sql and understand about this

After figuring out the password and giving it in the login page,you will get a rsa encrypted flag.Now how I found out that that this is RSA encrypted. Well all I see are numbers and the admin is a fool who cannot make a encryption of his own.(jk again you can see a keys table in the tables.txt from tux image and see columns n,e and phi which is only available in RSA).Again .. do sql injection to find out the keys and you can use the n,e and phi values to make a decrypt key and decrypt it(this is a bit of math and i'm not a math guy.If you are do the math if not find a website which will calculate d for you.) And using python [rsa_python](https://pypi.org/project/rsa-python/) for decryption.That's all You have the flag.

## Concepts Used Here

* Jwt Cracking
* RSA Encrytion
* Blind SQL Injection on SQLite3


