# Markov Chain Poetry
# Generated from poems by Emily Dickinson
import random
import sys
import re

poems = open("dickinson.txt", "r").read()
poems=poems.lower()
poems = poems.replace("\n\n"," ")
poems = poems.replace("\n"," \n ")
poems = re.sub(r'[^A-Za-z \n]', '', poems)
poems = ''.join([i for i in poems if not i.isdigit()]).split(' ')
# This process the list of poems. Double line breaks separate poems, so they are removed.
# Splitting along spaces creates a list of all words.

index = 1
chain = {}
prop = {}
output_count = 1000 # Desired word count of output
''' 
chain = {
    would:{have:1, dog:1},
    have:{pointed:1, cooled:1}
    dog{}

}

'''
# This loop creates a dicitonary called "chain". Each key is a word, and the value of each key
# is an array of the words that immediately followed it.
for word in poems[index:]: 
    key = poems[index - 1]
    if key in chain:
        word_stats = chain[key]
        if word in word_stats:
            word_stats[word] += 1
        else:
            word_stats[word] = 1
        word_stats["count"] += 1
    else:
        new_word_stats = {}
        new_word_stats[word]=1
        new_word_stats["count"] = 1
        chain[key] = new_word_stats
    

    index += 1


print("chain" , chain)
# print("probability:", chain["in"]["the"]/chain["in"]["count"])

word1 = random.choice(list(chain.keys())) #random first word
message = word1.capitalize()

# Picks the next word over and over until word count achieved
while len(message.split(' ')) < output_count:
    word_choice_array = [key for key in chain[word1] if key != 'count']
    counts_array = [value for key, value in chain[word1].items() if key != 'count']
    probability_array = [number / chain[word1]['count'] for number in counts_array]
    word2 = random.choices(word_choice_array, weights=probability_array)[0]
    word1 = word2 
    message += ' ' + word2

# creates new file with output and prints it to the terminal
with open("DKSN2_poem.txt", "w") as file:
    file.write(message)
output = open("DKSN2_poem.txt","r")
print(output.read())
/