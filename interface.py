import wikipedia

e = open("entities.txt", "r")
content = e.read()
entities = content.split("\n")[:-1]
e.close()

q = open("question.txt", "r")
question = q.read()
q.close()


entity_map = dict()


print(question)

for word in question.split():
    print("word: " + str(word))
    try:
        search_term = wikipedia.page(word)
        related = search_term.links
        suggestions = list(set(related) & set(entities))
        entity_map[word] = suggestions
    except:
        continue
print(entity_map)
