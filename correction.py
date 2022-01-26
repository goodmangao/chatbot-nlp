# -*- coding:utf-8 -*-
import re
from collections import Counter

# Convert all data to lowercase and remove special characters and read the existing database and count
count = Counter(re.findall(r'\w+', (open('D:/train/english_data.txt').read()).lower()))

# Calculate the probability of words appearing in the database
def probability1(word1, S=sum(count.values())):
    return count[word1] / S

# Edit a word
def current_w(sentence_words):
    sen = []
    all_letters = 'abcdefghijklmnopqrstuvwxyz'
    for word in sentence_words:
        if word in count:
            sen = sen+[word]
            continue
        else:
            separations = []
            for i in range(len(word) + 1):
                separations.append((word[:i], word[i:]))

            deletes = []           # delete a letter
            for front, back in separations:
                if back:
                    deletes.append(front + back[1:])

            swaps = []        # Swap front and back letter
            for front, back in separations:
                if len(back) > 1:
                    swaps.append(front + back[1] + back[0] + back[2:])

            substitutes = []          # substitutes a new letter
            for front, back in separations:
                if back:
                    for m in all_letters:
                        substitutes.append(front + m + back[1:])

            adds = []           # insert a letter
            for front, back in separations:
                for m in all_letters:
                    adds.append(front + m + back)

            word1 = set(deletes + swaps + substitutes + adds)

            a = []
            # The result word that requires edit distance is in the corpus
            for j in word1:
                if j in count:
                    a = a + [j]
            word1 = set(a)
            # If there are more than two spelling errors in the input or the input is correct but not in the vocabulary,
            # the original input will be output
            if word1 == set():
                sen = sen+list(word)
                continue
            sen = sen+[max(word1, key=probability1)]   # all words are brought into the P function and compared.
    return sen
