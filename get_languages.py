import requests
import bs4
import json

url = 'https://github.com/trending?l=java&since=monthly'
response = requests.get(url);
soup = bs4.BeautifulSoup(response.text)
langs = soup.findAll('div',{"role":"menuitem"})

results = []
for lang in langs:
	href = lang.find('a')["href"]
	text = lang.find('a').text
	startIndex = href.index('l=')+2
	endIndex = href.index('&')
	l = href[startIndex:endIndex]
	#print text
	#print l
	result = {}	
	result["name"] = text
	result["path"] = l
	results.append(result)

#print json.dumps(results)	
f = open("languages.json","w")
f.write(json.dumps(results))
f.close
	
