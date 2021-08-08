import re
string="검색결과 약 186개 (0.32초)"
string=string[:string.find('(')] 
string="".join(re.findall("\d+",string))
print(int(string))