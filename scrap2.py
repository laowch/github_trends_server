import requests
import bs4
import json
import time
from multiprocessing import Pool

def parse_repo_name(tag):
	repo_name = {}
	repo_name["href"] = tag.find("a")["href"]
	return repo_name

def parse_repo_description(tag):
	repo_des = {}
	repo_des["des"] = tag.text.strip()
	return repo_des
	
def parse_repo_meta(tag):
	repo_meta = {}
	contributors = []
	images = tag.findAll("img")
	for image in images:
		user = {}
		user["name"] = image["title"]
		user["avatar"] = image["src"]
		contributors.append(user)
	repo_meta["contributors"] = contributors
	metas = tag.text.split("\n")
	
	for meta in metas:
		if meta.find("star") >=0 :
			repo_meta["meta"] = meta.strip()
	return repo_meta
		
def parse_repo(url):
	response = requests.get(url);
	soup = bs4.BeautifulSoup(response.text,'html.parser')
	#repo_list = soup.find('ol',{"class":"repo-list"})
	repo_items = soup.findAll('li',{"class":"repo-list-item"})
	#print repo_items

	parsed_items = []

	for repo_item in repo_items:
		parsed_item = {}
		for tag in repo_item:
			#print type(tag)
			if type(tag) is bs4.element.Tag and "class" in tag.attrs:
				#print tag["class"][0]
				if tag["class"][0] == "repo-list-name":
					#print parse_repo_name(tag)
					parsed_repo_name = parse_repo_name(tag)
					parsed_item.update(parsed_repo_name)
				if tag["class"][0] == "repo-list-description":
					#print parse_repo_description(tag)
					parsed_repo_des = parse_repo_description(tag)
					parsed_item.update(parsed_repo_des)
				if tag["class"][0] == "repo-list-meta":
					#print parse_repo_meta(tag)
					parsed_repo_meta = parse_repo_meta(tag)
					parsed_item.update(parsed_repo_meta)
		parsed_items.append(parsed_item)
	if len(parsed_items) == 0:
		print url
		print response
		#print response.text
	return parsed_items

	

sinces = ['monthly']
url_head = 'https://github.com/trending?l='

def process_by_lang(lang):
	for since in sinces:
        	url = url_head + lang["path"] + "&since=" + since
                parsed_repos = parse_repo(url)
                f = open("json/"+lang["path"] + "_" + since,"w")
                f.write(json.dumps(parsed_repos))
                f.close()
		time.sleep(5)

def main():
	langs_file = open("languages.json","r")
	langs_json = langs_file.read()
	langs = json.loads(langs_json)
	pool = Pool(1)
	pool.map(process_by_lang,langs)

main()
