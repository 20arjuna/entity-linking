import wikipedia

my_file = open("entities.txt", "r")
content = my_file.read()
entities = content.split("\n")[:-1]
my_file.close()

entity_map = dict()
question = input("Enter your quizbowl question below" + "\n")

print("\n")

print(question)

for word in question.split("\n"):
    print("word: " + str(word))
    try:
        search_term = wikipedia.page(word)
        related = search_term.links
        suggestions = list(set(related) & set(entities))
        entity_map[word] = suggestions
    except:
        continue
print(entity_map)
