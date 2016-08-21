import json
sinces = ['monthly']
langs_file = open("languages.json","r")
langs_json = langs_file.read()
langs = json.loads(langs_json)
for lang in langs:
	f = open("json/"+lang["path"] + "_monthly","r")
	repos_json = f.read()
	#print repos_json
	total_count =0
	if repos_json:
		repos = json.loads(repos_json)
		for repo in repos:
			if "meta" in repo:
				#print repo["meta"]
				meta = repo["meta"]
				index = meta.index(" ")
				star_count = int(filter(str.isdigit,str(meta[0:index])))
				total_count = total_count + star_count
	print lang["path"]+"	" + lang["name"] +"	" + str(total_count)
	
