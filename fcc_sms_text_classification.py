# -*- coding: utf-8 -*-
"""fcc_sms_text_classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/freeCodeCamp/boilerplate-neural-network-sms-text-classifier/blob/master/fcc_sms_text_classification.ipynb
"""

import pandas as pd
!pip install tensorflow-datasets
import tensorflow_datasets as tfds
import numpy as np
import matplotlib.pyplot as plt

from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Flatten, Embedding, Dense
from keras.callbacks import EarlyStopping

# get data files
!wget https://cdn.freecodecamp.org/project-data/sms/train-data.tsv
!wget https://cdn.freecodecamp.org/project-data/sms/valid-data.tsv

train_file_path = "train-data.tsv"
test_file_path = "valid-data.tsv"

train_df = pd.read_csv (train_file_path, sep = '\t',names=['class','text'] )
test_df =  pd.read_csv (test_file_path, sep = '\t',names=['class','text'])

train_df.head()
test_df.head()

train_message = train_df["text"].values.tolist()
train_label = np.array([0 if x=="ham" else 1 for x in train_df['class'].values.tolist()])
test_message = test_df["text"].values.tolist()
test_label = np.array([0 if x=="ham" else 1 for x in test_df['class'].values.tolist()])

vocabulary_dict = {}
for message in train_message:
  for vocabulary in message.split():
    if vocabulary not in vocabulary_dict:
      vocabulary_dict[vocabulary] = 1
    else:
      vocabulary_dict[vocabulary] += 1
VOCAB_SIZE = len(vocabulary_dict)
MAX_LENGTH = len(max(train_message, key=lambda p: len(p.split())).split())

print(MAX_LENGTH)
print(VOCAB_SIZE)

encoded_train_message = [one_hot(d, VOCAB_SIZE) for d in train_message]
padded_train_message = pad_sequences(encoded_train_message, maxlen=MAX_LENGTH, padding='post')
encoded_test_message = [one_hot(d, VOCAB_SIZE) for d in test_message]
padded_test_message = pad_sequences(encoded_test_message, maxlen=MAX_LENGTH, padding='post')

model = Sequential()
embedding_layer = Embedding(VOCAB_SIZE, 100, input_length=MAX_LENGTH)
model.add(embedding_layer)
model.add(Flatten())
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
monitor = EarlyStopping(monitor='val_acc', min_delta=1e-4, patience=25, verbose=1, mode='max', restore_best_weights=True)
model.fit(padded_train_message, train_label, validation_data=(padded_test_message, test_label), callbacks=[monitor], epochs=1000, verbose=2)

# function to predict messages based on model
def predict_message(pred_text):
  class_dict = {
      0 : "ham",
      1 : "spam",
      }
  encoded_message = [one_hot(pred_text, VOCAB_SIZE)]
  padded_message = pad_sequences(encoded_message, maxlen=MAX_LENGTH, padding='post')
  prediction = [model.predict(padded_message)[0][0], class_dict[np.round(model.predict(padded_message)[0][0])]]
  return prediction

pred_text = "you have won 10000€?"

prediction = predict_message(pred_text)
print(prediction)

# Run this cell to test your function and model. Do not modify contents.
def test_predictions():
  test_messages = ["how are you doing today",
                   "sale today! to stop texts call 98912460324",
                   "i dont want to go. can we try it a different day? available sat",
                   "our new mobile video service is live. just install on your phone to start watching.",
                   "you have won £1000 cash! call to claim your prize.",
                   "i'll bring it tomorrow. don't forget the milk.",
                   "wow, is your arm alright. that happened to me one time too"
                  ]

  test_answers = ["ham", "spam", "ham", "spam", "spam", "ham", "ham"]
  passed = True

  for msg, ans in zip(test_messages, test_answers):
    prediction = predict_message(msg)
    if prediction[1] != ans:
      passed = False

  if passed:
    print("You passed the challenge. Great job!")
  else:
    print("You haven't passed yet. Keep trying.")

test_predictions()