import re


AI_OUTPUT = """ Hello Murali
 Your email address is murali@example.com
 test@gmail.com  and IPV4 is 172.16.0.1 """

#username@domain.tld
#username a-zA-Z 0-9 _
#domain a-zA-Z 0-9
#tld a-z0-9

#result = re.search(r'[a-zA-Z0-9_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+', AI_OUTPUT)
#result = re.findall(r'[a-zA-Z0-9_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+', AI_OUTPUT)
#result = re.subn(r'\w+@\w+\.\w+', 'EMAIL_REDACTED', AI_OUTPUT)
result = re.subn(r'\d+\.\d+\.\d+\.\d+', 'REDACTED_IPV4', AI_OUTPUT)
print(result)    