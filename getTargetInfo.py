import  re
content = "电话号码:15555245698 qwertyuiopQQ:1524252226 邮箱：555dd-s@qq.com 固定电话:0931-8525555 短号码：555555"
infos = set()
results = re.findall(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}|1[3|4|5|7|8]\d{9}|\d{5,10}|0\d{2,3}-\d{5,9}\b",content)
for result in results:
    if re.match(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}",result) != None:
        result = "[email:"+result+"]"
        infos.add(result)
    elif (re.match(r"1[3|4|5|7|8]\d{9}",result) != None)or(re.match(r"0\d{2,3}-\d{5,9}",result) != None):
        result = "[phone:"+result+"]"
        infos.add(result)
    else:
            result = "[qq:"+result+"]"
            infos.add(result)

for info in infos:
    print(info)