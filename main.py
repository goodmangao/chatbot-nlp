import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from correction import current_w
from nltk import word_tokenize, pos_tag
import time
from weather import weather
from game1 import game1

lemmatizer = WordNetLemmatizer()
# read json
qandas = json.loads(open('output.json').read())
chats=json.loads(open('output2.json').read())
# read file
text_tokens = pickle.load(open('text_tokens.pk1', 'rb'))
classes = pickle.load(open('classes.pk1', 'rb'))
model = load_model('machinemodel2.h5')

judge1 = True
judge2 = True
judge = True

print('The bot is on')

# Identity management
print('BOT: Hi, what is your name?')
text = input('')
tokens = word_tokenize(text)
post = pos_tag(tokens)
name = ''
for n in range(len(post)):         # Find the name in the sentence
    if post[n][1] == 'NNP':
        name = name+' '+post[n][0]
print(f'BOT: Hi,{name}')
print("BOT:please input 'chat','question and answer','date', 'play games' and 'weather' ")  # Intent matching

while (judge == True) :
    sentence = input('')

    if (sentence == 'bye'):
        judge = False
        print(f"BOT: Bye!{name}, good luck!")
        break                             # Meet the conditions and end the conversation

    if (sentence == 'chat'):              # Intent matching :Small talk
        judge1 = True
        print(f"BOT: Ok,{name},Let's have a chat")
        while (judge1 == True):
            sentence = input('')

            # back to previous step
            if (sentence == 'back to previous step'):
                judge1 = False
                print("BOT: please input 'chat','question and answer','date', 'play games' and 'weather'")
                break
            # end the conversation
            if (sentence == 'bye'):
                judge = False
                print(f"BOT: Bye!{name}, good luck!")
                break
            # Begin to chat
            else:
                # Split the input sentence
                sentence_words = nltk.word_tokenize(sentence)
                # Convert all data to lowercase and remove special characters, read existing database and count
                sentence_words = current_w(sentence_words)    # Correction of possible mistyped words
                # Lemmatisation
                sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
                # Preparing the Bag-of-Words and make a match
                bag = [0] * len(text_tokens)
                for w in sentence_words:
                    for i, word in enumerate(text_tokens):
                        if word == w:
                            bag[i] = 1

                bow = np.array(bag)
                rate = model.predict(np.array([bow]))[0]   # Predict probability by model
                ERROR_THRESHOLD = 0.55
                # Get the corresponding label that meets the probability requirement
                results = [[i, r] for i, r in enumerate(rate) if r > ERROR_THRESHOLD]
                # print(results)
                results.sort(key=lambda x: x[1], reverse=True)
                return_list = []
                result = ''
                for r in results:
                    return_list.append({'qanda': classes[r[0]], 'probablity': str(r[1])})
                # Find the answer under the corresponding label
                if return_list!=[]:
                    tag = return_list[0]['qanda']
                    list_of_qandas = chats['qandas']
                    for i in list_of_qandas:
                        if i['label'] == tag:
                            result = random.choice((i['answer']))
                            print(f"BOT:{result}")
                    # If the result is empty, it means that the model can find the corresponding answer in the
                    # question and answer function
                    if result == '':
                        print("BOT:Please 'back to previous step' and choose 'question and answer' to ask question")
                # If the result is empty,the robot cannot find the corresponding answer in the database
                else:
                    print(f"BOT:I am sorry,{name}, I don't understand you")

    if (sentence == 'question and answer'):      # Intent matching: question and answer
        print(f"BOT: Ok,{name},please ask questions")
        judge2 = True
        while (judge2 == True):
            sentence = input('')
            if (sentence == 'back to previous step'):
                judge2 = False
                print("BOT: please input 'chat','question and answer','date', 'play games' and 'weather'")
                break

            if (sentence == 'bye'):
                judge = False
                print(f"BOT: Bye!{name}, good luck!")
                break
            else:

                sentence_words = nltk.word_tokenize(sentence)
                sentence_words = current_w(sentence_words)
                sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]

                bag = [0] * len(text_tokens)
                for w in sentence_words:
                    for i, word in enumerate(text_tokens):
                        if word == w:
                            bag[i] = 1

                bow = np.array(bag)
                rate = model.predict(np.array([bow]))[0]
                ERROR_THRESHOLD = 0.55
                results = [[i, r] for i, r in enumerate(rate) if r > ERROR_THRESHOLD]
                results.sort(key=lambda x: x[1], reverse=True)
                return_list = []
                result = ''
                for r in results:
                    return_list.append({'qanda': classes[r[0]], 'probablity': str(r[1])})
                if (return_list!=[]):
                    tag = return_list[0]['qanda']
                    list_of_qandas = qandas['qandas']
                    for i in list_of_qandas:
                        if i['label'] == tag:
                            result = random.choice((i['answer']))
                            print(f"BOT:{result}")
                    if result=='':
                        print("BOT:Please 'back to previous step' and choose 'chat' to have a chat with me")

                else:
                    print(f"BOT:I am sorry,{name}, I don't understand you")

    if (sentence == 'date'):                  # Intent matching: 'date'
        # query time and date
        print(time.ctime())
        print("BOT:please input 'chat','question and answer','date', 'play games' and 'weather'")
        continue

    if (sentence == 'weather'):                # Intent matching: 'weather'
        # query weather
        weather()
        print("BOT:please input 'chat','question and answer','date', 'play games' and 'weather'")
        continue

    if (sentence == 'play games'):              # Intent matching: 'play games'
        # play games
        print('BOT:Welcome to play "Dice GAME"')
        game1()
        print("BOT:please input 'chat','question and answer','date', 'play games' and 'weather'")
        continue

