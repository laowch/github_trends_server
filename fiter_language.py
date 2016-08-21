import json
rank_file = open("rank.txt","r")
rank_str = rank_file.read()
ranks = rank_str.split("\n")

langs_file = open("languages.json","r")
langs_json = langs_file.read()
langs = json.loads(langs_json)

ranked_langs = []
for rank in ranks:
	#print rank
	for lang in langs:
		if lang["name"] == rank:
			ranked_langs.append(lang)
			break
ranked_langs.sort()
print ranked_langs
f = open("langs.json","w")
f.write(json.dumps(ranked_langs))
f.close

