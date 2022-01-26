# -*- coding:utf-8 -*-
import nltk
# nltk.download('stopwords')
import numpy as np
import random
import json
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
os.environ["CUDA_VISIBLE_DEVICES"] = '0'

# File preprocessing
lemmatizer= WordNetLemmatizer()
# question and answer
text_tokens1 = []
classes1 = []
tags1 = []
# chat
text_tokens2 = []
classes2 = []
tags2 = []
stopletter = ['.',',','?']  # 'text_tokens2' stopwords
# together
text_tokens = []
classes = []
tags = []
# question and answer
qandas = json.loads(open('output.json').read())  # read output.json
for qanda in qandas['qandas']:        # Extract tags in json
    for ques in qanda['question']:    # Find the tag of 'question'
        word_list1 = nltk.word_tokenize(ques)   # Segment each ques of word
        text_tokens1.extend(word_list1)
        tags1.append((word_list1, qanda['label']))   # put label and question together
        if qanda['label'] not in classes1:
            classes1.append(qanda['label'])   # put label in classes
# chat
chats = json.loads(open('output2.json').read())
for chat in chats['qandas']:
    for ques in chat['question']:
        word_list2 = nltk.word_tokenize(ques)
        text_tokens2.extend(word_list2)
        tags2.append((word_list2, chat['label']))
        if chat['label'] not in classes2:
            classes2.append(chat['label'])
# Lowercase all letters and remove stop words, stop words under different functions are different
text_tokens1 = [word.lower() for word in text_tokens1 if not word in stopwords.words()]
text_tokens2 = [word.lower() for word in text_tokens2 if not word in stopletter]
text_tokens = text_tokens1+text_tokens2
text_tokens = [lemmatizer.lemmatize(word) for word in text_tokens]
text_tokens = sorted(set(text_tokens))

classes = classes1+classes2
classes = sorted(set(classes))

pickle.dump(text_tokens, open('text_tokens.pk1', 'wb'))  # put all
pickle.dump(classes, open('classes.pk1', 'wb'))

training = []
zero = [0]*len(classes)
tags = tags1+tags2
# Preparing the Bag-of-Words
for tag in tags:
    bag = []
    word_question = tag[0]
    word_question = [lemmatizer.lemmatize(word.lower()) for word in word_question]
    for word in text_tokens:
        bag.append(1) if word in word_question else bag.append(0)
    export_list = list(zero)
    export_list[classes.index(tag[1])] = 1
    training.append([bag, export_list])
# Prepare the training set
random.shuffle(training)
training = np.array(training)
train_x = list(training[:, 0])
train_y = list(training[:, 1])
# Training model by tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
# Build model
model = Sequential()
model.add(Dense(3000, input_shape=(len(train_x[0]),), activation='relu'))        # Fully connected layer
model.add(Dropout(0.4))             # Prevent overfitting
model.add(Dense(2000, activation='relu'))     # Fully connected layer
model.add(Dropout(0.4))             # Prevent overfitting
# softmax apply to multi-category problems to make the big bigger
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-7, momentum=0.9, nesterov=True)    # Optimizer (stochastic gradient descent)
# Specify the optimizer object, loss function, and evaluation index used by the network through the compile function
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Send the data to be trained and the data set for verification through the fit() function
mind = model.fit(np.array(train_x), np.array(train_y), epochs=150, batch_size=10, verbose=1)
model.save('machinemodel2.h5', mind)    # save model
print('Done')
