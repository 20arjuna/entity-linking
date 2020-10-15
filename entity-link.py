import tagme

tagme.GCUBE_TOKEN = "a3cfadd0-cd8b-40a6-8cf2-db83d77692a0-843339462"

print("Annotation\n")
lunch_annotations = tagme.annotate("Leonard Bernstein described this composer as “a little German-Czech- Moravian-Jewish-Polish boy.” Reputed to have adopted his mother’s limp, he actually changed the rhythm of his steps to suit the tunes constantly drifting through his head. After a brief affair with the daughter of the telegraph operator of his hometown of Iglau, he composed the orchestral work The Song of the Earth. Inspired by Nietzsche, he wrote his 3rd symphony entitled The Joyful Science, which contains a passage based upon Thus Spake Zarathustra. For 10 points, name the composer best known for massive symphonies such as his Eighth, the Symphony of a Thousand.")

# Print annotations with a score higher than 0.1
for ann in lunch_annotations.get_annotations(0.1):
    print(ann)

print("\n\n\nMention Finding\n")

tomatoes_mentions = tagme.mentions("Leonard Bernstein described this composer as “a little German-Czech- Moravian-Jewish-Polish boy.” Reputed to have adopted his mother’s limp, he actually changed the rhythm of his steps to suit the tunes constantly drifting through his head. After a brief affair with the daughter of the telegraph operator of his hometown of Iglau, he composed the orchestral work The Song of the Earth. Inspired by Nietzsche, he wrote his 3rd symphony entitled The Joyful Science, which contains a passage based upon Thus Spake Zarathustra. For 10 points, name the composer best known for massive symphonies such as his Eighth, the Symphony of a Thousand.")

for mention in tomatoes_mentions.mentions:
    print(mention)
