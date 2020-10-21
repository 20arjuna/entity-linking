import tagme
import json
import sys
import subprocess as sub

tagme.GCUBE_TOKEN = "a3cfadd0-cd8b-40a6-8cf2-db83d77692a0-843339462"

def generate_json(pd, json_file):
    q = open("packet_data/" + pd, "r")
    content = q.read()
    questionList = content.split("\n")
    q.close()

    jsonData = {}
    jsonData['entities'] = []
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
            with open("json_data/" + json_file, 'w') as outfile:
                outfile.write(json_object)   
        i+=1
        
if __name__ == '__main__':
    # for arg in sys.argv[1:]:
    packet_data = sys.argv[1]
    print(packet_data)
    json_file = sys.argv[2]

    for i in range(2,13):
        generate_json("athena" + str(i) + ".txt", "athena" + str(i) + ".json")
    
    for j in range(1, 5):
        generate_json("pace" + str(j) + ".txt", "pace" + str(j) + ".json")
    
    for x in range(1, 5):
        generate_json("scop" + str(x) + ".txt", "scop" + str(x) + ".json")
    
    for y in range(1, 5):
        generate_json("bhsat" + str(y) + ".txt", "bhsat" + str(y) + ".json")


    
    

