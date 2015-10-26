__author__ = 'wangdiyi'
"""
Minimal character-level Vanilla RNN model. Written by Andrej Karpathy (@karpathy)
BSD License
"""
import numpy as np
import pickle
import random
import time
from collections import Counter

#read
f1 = open("./data_NextBasket.txt", "rb")
data = pickle.load(f1)
f1.close()
# data.get(3)
f1 = open("./data_idList.txt", "rb")
listfre = pickle.load(f1)
f1.close()
f1 = open("./list_cust4List.txt", "rb")
listcust = pickle.load(f1)
f1.close()
f1 = open("./list_product_id.txt", "rb")
product_id = pickle.load(f1)
f1.close()
print len(listcust)
dict=Counter(listfre)
frelist=sorted(dict.items(), key=lambda e:e[1], reverse=True)
fre=[]
for i in range(80):
	fre.append(frelist[i][0])


# hyperparameters
hidden_size = 10 # size of hidden layer of neurons
learning_rate = 1e-1
goods_size = 1559
itert = 0
top = 50

# model parameters
u = np.random.randn(hidden_size, hidden_size)*0.5 # input to hidden
w = np.random.randn(hidden_size, hidden_size)*0.5 # hidden to hidden
t = np.random.randn(goods_size, hidden_size)*0.5 # one-hot to embedding


def sigmoid(x):                  #sigmoid function
	return 1.0/(1+np.exp(-x))


def lossFun(inputs, targets, negtargets, hprev)                    :#loss function    everybasket
	loss = 0
	mid = 0
	midn = 0
	midt = 0
	hl = np.copy(hprev)
	x = np.zeros((goods_size,1))
	tx= np.zeros((hidden_size,1))# the result of (t.T,x),shape is the same as the h

	# forward pass
	#time1=time.clock()
	for i in inputs:
		x[i-1][0]=1
		for j in range(hidden_size):
			tx[j][0]+=t.T[j][i-1]
	h = sigmoid(np.dot(u,tx)+ np.dot(w,hl)) # hidden state
	#time2=time.clock()
	du, dw, dt = np.zeros_like(u), np.zeros_like(w), np.zeros_like(t)



	for i in targets:                   #loss to hide
		xt = np.zeros((hidden_size,1))# the result of (x.T,t).T
		xh= np.zeros((goods_size,hidden_size))#the result of (x, h.T),shape is the same as the t
		for j in range(hidden_size):
			xt.T[0][j]=t[i-1][j]
		xh[i-1]=h.T
		# mid += 1-sigmoid(np.dot((np.dot(np.dot(x.T, t), h)), np.dot(x.T,t))).T
		mid += (1-sigmoid(np.dot(xt.T,h)))* xt
		midt += (1-sigmoid(np.dot(xt.T, h))) *xh

	for i in negtargets:
		xn= np.zeros((hidden_size,1))
		xh= np.zeros((goods_size,hidden_size))
		for j in range(hidden_size):
			xn.T[0][j]=t[i-1][j]
		xh[i-1]=h.T
		mid -= sigmoid(np.dot(xn.T,h))*xn
		midn +=sigmoid(np.dot(xn.T,h))* xh
	#time4=time.clock()
	dw = np.dot(mid*h*(1-h),hl.T)
	du += np.dot(mid*h*(1-h), tx.T)         #x how to choose   x x+1
	dt += np.dot(np.dot(u.T,mid*h*(1-h)),x.T).T
	#time5=time.clock()
	dt +=midt-midn
	# dt = np.dot(np.dot((1 - sigmoid(np.dot(np.dot(x.T,t), h))),x),h.T) + midn + \
	#      np.dot(np.dot(mid.T*hl*(1-hl), u.T), x.T)
	hl = h
	#print (time2-time1),(time3-time2),(time4-time3),(time5-time4)
	return loss, du, dw, dt, hl


def negasamp(targets):
	# list2 = product_id
	# negtargets=random.sample(list2,80)
	# for i in targets:
	# 	negtargets = filter(lambda a: a != i, negtargets)
	# negtargets = negtargets[0:50]
	# return negtargets

	# negtargets = fre[0:-1]
	# for i in targets:
	# 	if i in negtargets:
	# 		negtargets.remove(i)
	# return negtargets[:50]
	negtargets = []
	return negtargets



def predict(customer, u, w, t):

	right = 0
	hl = np.zeros((hidden_size, 1))
	x = np.zeros((goods_size,1)) # encode in 1-of-k representation
	xt = np.zeros((goods_size,1)) # encode in 1-of-k representation
	# rank = np.zeros((20,2))
	rank = [[0]*2 for row in range(top)]
	allrank = [[0]*2 for row in range(len(product_id))]

	for j in range(len(customer)-1):
		inputs = customer[j]
		for i in inputs:
			x[i-1][0] = 1
		h = sigmoid(np.dot(np.dot(u,t.T),x) + np.dot(w,hl)) # hidden state

	for j in range(len(customer)-1, len(customer)):
		targets = customer[j]
		valuet=0
		for i in targets:
			xt[i-1][0] = 1
			valuet += sigmoid(np.dot(np.dot(xt.T,t),h))
			xt = np.zeros((goods_size,1))
		avr=valuet/len(targets)


		# hl = h
		# x = np.zeros((goods_size,1))
		#
		# for i in targets:
		# 	x[i-1][0] = 1
		# h = sigmoid(np.dot(np.dot(u,t.T),x) + np.dot(w,hl)) # hidden state

	return avr

while True:
	avr = 0
	# rightpre= -100
	itert += 1
	# timec = time.clock()
	# time1=0
	# time2=0
	# for i in range(len(listcust)-1):
	# 	customer = data[listcust[i]]
	# 	hprev = np.zeros((hidden_size, 1))
	#
	# 	for j in range(len(customer)-1):
	#
	# 		inputs = customer[j]
	# 		targets = customer[j+1]
	# 		timeb=time.clock()
	#
	# 		negtargets = negasamp(targets)
	# 		# print "b"
	# 		# print timeB-timeb
	#
	# 		loss, du, dw, dt, hprev = lossFun(inputs, targets, negtargets, hprev)
	# 		# print "c"
	# 		# print timec-timeB
	# 		#time3=time.clock()
	# # for j in range(len(inputs)-1):
	# #     # print "basket"
	# #     # print j
	# #     loss, du, dw, dt, hprev = lossFun(inputs, targets, negtargets, hprev)
	# 		for param, dparam in zip([u, w, t],[du, dw, dt]):
	# 			param += learning_rate * dparam # adagrad update
	# 		#time4=time.clock()
	# print time1
	# print time2
	# timea = time.clock()
	# print "a-c"
	# print timea - timec
	# for i in range(len(listcust)-1):
	# 	customer = data[listcust[i]]
	# 	print len(listcust)
	# 	time1 = time.clock()
	# 	right += predict(customer, u, w, t)
	# 	time2 = time.clock()
	# 	print i
	# 	print "eachcustpre"
	# 	print time2-time1
	# timeA = time.clock()
	# print "allcustpre"
	# print timeA - timea
	# print right
	f1 = open("./resultu.txt", "r")
	u = pickle.load(f1)
	f1.close()
	f1 = open("./resultw.txt", "r")
	w = pickle.load(f1)
	f1.close()
	f1 = open("./resultt.txt", "r")
	t = pickle.load(f1)
	f1.close()
	try:
		if itert % 1 == 0:
			avr=0
			for i in range(len(listcust)-1):
				customer = data[listcust[i]]
				avr += predict(customer, u, w, t)
			avr=avr/len(listcust)
			print "Average is %f"%avr		

			
		print "iter %d" % itert
		
	except:
		continue






