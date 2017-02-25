from urllib.request import urlopen
from bs4 import BeautifulSoup
"""
    需求：
        获取子页面正文文本及用户ID
        <div class="post_bubble_middle" style="background:url(http://tb1.bdstatic.com/tb/cms/post/bubble/qingren_2.png)">须知：...</div>
        <div id="post_content_103351141195" class="d_post_content j_d_post_content clearfix"> 往事如风 如风往事 烟消云散</div>

        <a class="p_author_face " style="" target="_blank" href="/home/main?un=%E5%BE%AE%E7%AC%91%E5%B0%8F%E9%98%BF%E5%AE%81&ie=utf-8&fr=pb&ie=utf-8"></a>
        获取子页面评论文本及用户ID
        <span class="lzl_content_main">联系方式</span>

        <a class="at j_user_card " data-field="{'un':'瑕安'}" alog-group="p_author" target="_blank" href="/home/main?un=%E7%91%95%E5%AE%89&ie=utf-8&fr=pb" username="瑕安">瑕安</a>
"""
outputStr = input("请输入采集结果输出路径：")
print("输出路径为"+outputStr)
output_file_name = outputStr+'/result.txt'
file = open(output_file_name,'a')
secondlink = "http://tieba.baidu.com/p/4962273429"
html = urlopen(secondlink)
bsObj = BeautifulSoup(html,"html5lib")
#得到子页面div
sonDivs = bsObj.findAll("div",{"class":{"l_post j_l_post l_post_bright noborder ","l_post j_l_post l_post_bright "}})
for sonDiv in sonDivs:
    #将sonDiv重新封装成bsObj(将二级页面子页面重装为一个新的html文档方便降低调用成本)
    sonHtml = "<html><head></head><body>"+str(sonDiv)+"</body></html>"
    sonBsObj = BeautifulSoup(sonHtml,"html5lib")

    #得到用户主页尾URL
    targetUrl = sonBsObj.find("a",{"class":{"p_author_face "}})
    if 'href' in targetUrl.attrs:
        userMainPageUrl = targetUrl.attrs['href']
        print(userMainPageUrl+":")

    content = sonBsObj.find("div",{"class":{"l_post j_l_post l_post_bright noborder ","l_post j_l_post l_post_bright "}}).get_text()
    print(content)
    file.write(content)
