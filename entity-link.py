import tagme

tagme.GCUBE_TOKEN = "a3cfadd0-cd8b-40a6-8cf2-db83d77692a0-843339462"

q = open("packet_data.txt", "r")
content = q.read()
questionList = content.split("\n")
q.close()

jsonData = {}
jsonData['entity'] = []

for question in questionList:
    print("reading: " + question[:10] + " ... ")
    annotation = tagme.annotate(question)
    for ann in annotation.get_annotations(0.1):
        jsonData['entity'].append(ann)
    
    with open('ATHENA_1.json', 'w') as outfile:
        json.dump(jsonData, outfile)

