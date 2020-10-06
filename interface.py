import wikipedia

my_file = open("entities.txt", "r")
content = my_file.read()
entities = content.split("\n")[:-1]
my_file.close()

entity_map = dict()
question = input("Enter your quizbowl question below" + "\n")

for word in question.split():
    search_term = wikipedia.page(word)
    related = search_term.content
    suggestions = list(set(related) & set(entities))
    entity_map[word] = suggestions

print(entity_map)
