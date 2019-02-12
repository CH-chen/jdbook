url1 = "//list.jd.com/1713-3258-3297.html"
url2 = "https://list.jd.com/list.html?cat=1713,3258,3297&tid=3297"
num1 = url1.rsplit('/')[3].rsplit('.')[0].rsplit('-')[0]
num2 = url1.rsplit('/')[3].rsplit('.')[0].rsplit('-')[1]
num3 = url1.rsplit('/')[3].rsplit('.')[0].rsplit('-')[2]

url3 = "https://list.jd.com/list.html?cat={},{},{}&tid={}".format(num1,num2,num3,num3)
print(url3)