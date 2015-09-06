__author__ = 'wangdiyi'
"""
Minimal character-level Vanilla RNN model. Written by Andrej Karpathy (@karpathy)
BSD License
"""
import numpy as np
import xlrd
import xlwt
data = xlrd.open_workbook('./test.xlsx') # should be simple plain text file
table = data.sheets()[0]
data = table.col_values(1)
chars = list(set(data))
data_size, movie_size = len(data), len(chars)
print 'data has %d characters, %d unique.' % (data_size, movie_size)
char_to_ix = { ch:i for i,ch in enumerate(chars) }
ix_to_char = { i:ch for i,ch in enumerate(chars) }

# hyperparameters
hidden_size = 100 # size of hidden layer of neurons
learning_rate = 1e-1

# model parameters
Wxh = np.random.randn(hidden_size, movie_size)*0.01 # input to hidden
Whh = np.random.randn(hidden_size, hidden_size)*0.01 # hidden to hidden
Why = np.random.randn(movie_size, hidden_size)*0.01 # hidden to output
def lossFun(inputs, targets, hprev):
  """
  inputs,targets are both list of integers.
  hprev is Hx1 array of initial hidden state
  returns the loss, gradients on model parameters, and last hidden state
  """
  x, y, p = [], [], []
  hl=hprev
  loss = 0
  # forward pass

  x = np.zeros((movie_size,1)) # encode in 1-of-k representation
  x[inputs-1][0] = 1
  print "x:"
  print x
  h = np.tanh(np.dot(Wxh, x) + np.dot(Whh, hl)) # hidden state
  print "h:"
  print h
  y = np.dot(Why, h) # unnormalized log probabilities for next chars
  print "y:"
  print y
  p = np.exp(y) / np.sum(np.exp(y)) # probabilities for next chars
  print "p:"
  print p
  loss=p[targets][0]

  dWxh, dWhh, dWhy = np.zeros_like(Wxh), np.zeros_like(Whh), np.zeros_like(Why)


  dy = np.copy(p)
  dy[targets][0] -= 1 # backprop into y
  for i in range(len(dy)):
      dy[i][0]=-dy[i][0]
  dWhy += learning_rate*np.dot(dy, h.T)
  dh = np.dot(Why.T, dy) # backprop into h
  dhraw = (1-h * h) * dh # backprop through tanh nonlinearity
  dWxh += learning_rate*np.dot(dhraw, x.T)
  dWhh += learning_rate*np.dot(dhraw, hl.T)
  for dparam in [dWxh, dWhh, dWhy]:
    np.clip(dparam, -5, 5, out=dparam) # clip to mitigate exploding gradients
  return loss, dWxh, dWhh, dWhy, h


for i in range(len(data)-1):
  if i == 0:
    hprev = np.ones((hidden_size,1)) # reset RNN memory
  inputs = char_to_ix[data[i]]
  targets = char_to_ix[data[i+1]]
  loss, dWxh, dWhh, dWhy, hprev = lossFun(inputs, targets, hprev)
  Wxh, Whh, Why=dWxh, dWhh, dWhy

