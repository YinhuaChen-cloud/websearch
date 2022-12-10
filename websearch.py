import urllib.request
import re

webaddr = "https://dblab.xmu.edu.cn/blog/924/" # 要搜素的网站根网页
searchstr = "apply" # 要搜索的字符串
depth = 1 # 搜索深度，防止出现递归搜索 TODO: 目前搜索深度只支持1，以后可以再改进

def getHtml(url):
  page = urllib.request.urlopen(url)
  html = page.read()
  return html

if __name__ == "__main__":
  urllist = [] # 用来存放包含被搜索字符串的网页标题, 除了根网页是用 url 的形式 

  html = getHtml(webaddr)
  htmlstr = html.decode("utf-8")

  # 在html文件中搜寻字符串
  results = re.findall(searchstr, htmlstr)
  if results:
    urllist.append(webaddr)

  # 在html文件中查找超链接, 存到一个列表里
  # eg: <a href="http://dblab.xmu.edu.cn/post/10164/">点击这里查看大数据学习路线图（大数据学习的最佳路径）</a></p>
  hrefs = re.findall("<a href=\".*\">.*</a>", htmlstr)

  # 生成一个字典，(key, val) = (超链接，中文标题)
  urltitledict = {}
  for ahref in hrefs:
    theurl = re.search("(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?", ahref, re.IGNORECASE)
    thetitle = re.search("<a href=\".*\">(.*)</a>", ahref, re.IGNORECASE)
    urltitledict[theurl.group(0)] = thetitle.group(1)

  # 遍历获得的超链接列表，进行depth=1的字符串匹配
  for key in urltitledict.keys():
    try:
      if(not re.findall("http", key)):
        continue
      html = getHtml(key)
      htmlstr = html.decode("utf-8")
      results = re.findall(searchstr, htmlstr)
      if results:
        urllist.append(urltitledict[key])
    except:
      print("a small error")

  for title in urllist:
    print(title)

 