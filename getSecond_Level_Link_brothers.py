from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
"""
    <li class="l_reply_num" style="margin-left:8px">
        <span class="red" style="margin-right:3px">123073</span>回复贴，共
        <span class="red">4085</span>页
    </li>
"""
secondLink = "http://tieba.baidu.com/p/4933481863"
secondLinkBrothers = set()
secondLinkBrothers.add(secondLink)
firstSecondHtml = urlopen(secondLink)
fisrtBsObj = BeautifulSoup(firstSecondHtml,"html5lib")
#拿到子页面最后一页URL结尾数字
minNum = 2147483647
for li in fisrtBsObj.findAll("li",{"class":"l_reply_num"}):
    liContent = li.get_text()
    #正则提取最小数字
    targetNums = re.findall("[0-9]{1,10}",liContent)
    for targetNum in targetNums:
        targetNum = int(targetNum)
        if(targetNum<minNum):
            minNum = targetNum

lastSonPageNum = minNum
pn = 2
for num in range(2,lastSonPageNum+1):
    #拼接二级自链接兄弟链接并保存
    brotherLink = "http://tieba.baidu.com/p/2823830811?pn="+ str(pn)
    pn = pn + 1
    secondLinkBrothers.add(brotherLink)