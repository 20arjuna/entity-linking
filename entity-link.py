import tagme
import json

tagme.GCUBE_TOKEN = "a3cfadd0-cd8b-40a6-8cf2-db83d77692a0-843339462"

q = open("packet_data.txt", "r")
content = q.read()
questionList = content.split("\n")
q.close()

jsonData = {}
jsonData['entities'] = {}
i = 1
for question in questionList:
    #jsonData['entity']['question ' + str(i)] = []
    print("reading: " + question[:10] + " ... ")
    annotation = tagme.annotate(question)
    for ann in annotation.get_annotations(0.1):
        #print(ann.__str__())
        #print(str(ann))
        #jsonData['entity']['question ' + str(i)].append(ann.__str__())
        jsonData['entities'].append(ann.__str__())
        json_object = json.dumps(jsonData, indent = 4)
        with open('ATHENA_1.json', 'w') as outfile:
            outfile.write(json_object)
        
    i+=1
    
    # print(type(jsonData))
    #print((jsonData))

    

