import itertools
import random
from random import shuffle
import math


def order_isomorphic(a, b):
  #check whether or not two permutations a and b are order isomorphic
  n = len(a)
  for i in range(0, n - 1):
    for j in range(i + 1, n):
      if ((a[i] < a[j] and b[i] > b[j]) or (a[i] > a[j] and b[i] < b[j])):
        return False
  return True


def permutations(T):
  #returns all permutations of a list T
  x = list(set(list(itertools.permutations(T))))
  res = []
  for i in x:
    perm = []
    for j in i:
      perm.append(j)
    res.append(perm)
  return res


def aligned_subsequences(k, t):
  #returns the subsequences of a list t that include the first element of length k
  #rationale for including first element is that in our stack_sort, the only violations of the restricted stack configs are going to include the first element, as otherwise we would've popped out on the previous turn
  x = list(set(list(itertools.combinations(t[:-1], k - 1))))
  res = []
  for i in x:
    perm = []
    for j in i:
      perm.append(j)
    perm.append(t[-1])
    res.append(perm)
  return res


#print(aligned_subsequences(3, [1,2,3,4,5]))


def stack_sort(p, T):
  #sort an input permutation p with map s_T
  #T is the list of permutations to avoid; i.e. T = {[2,1]} for non-restricted stack sort
  res = []
  stack = []
  index = 0
  while (len(res) + len(stack) != len(p)):
    avoiding = True
    if (len(stack) == 0):
      stack.append(p[index])
      index += 1
    else:
      stack.append(
        p[index]
      )  #create hypothetical new stack, check if it contains anything in T4
      for t in T:
        for i in aligned_subsequences(len(t), stack):
          if (
              order_isomorphic(t[::-1], i)
          ):  #reverse everything in t since using list to store stack inherently makes reading go bottom up
            avoiding = False
      if (avoiding == True):
        index += 1  #no issues, move on
      if (avoiding == False):
        stack.pop()  #remove hypothetical element
        k = stack.pop()  #append original top to res
        res.append(k)
        #don't increase index, since we are still on the same element
    #print(res, stack)
  while (len(stack) > 0):
    k = stack.pop()
    res.append(k)
  return res


def machine(p, sigma, tau):
  #perform the (sigma, tau)-machine on permutation p
  return stack_sort(stack_sort(p, [sigma, tau]), [[2, 1]])


def s(p):
  return stack_sort(p, [[2, 1]])  #normal sort


def list_n(n):
  return [i for i in range(1, n + 1)]


def hat(p):
  #returns the "hat" of a permutation p
  res = []
  res.append(p[1])
  res.append(p[0])
  for i in p[2:]:
    res.append(i)
  return res


#how many applications to return a permutation to the identity?


def comp(p):
  new = []
  for i in p:
    new.append(len(p) + 1 - i)
  return new


def half_increasing(p):
  return half_decreasing(comp(p))


def half_decreasing(p):
  index = 1
  for j in range(len(p) - 2, 0, -2):
    if p[j] != index:
      return False
    index += 1
  return True

def contains(p, t):
  #check if perm p contains t
  x = list(set(list(itertools.combinations(p, len(t)))))
  for i in x:
    if order_isomorphic(i, t):
      return True
  return False
  

def half_decr(p):
  #print how much of the permutation is in half decreasing mode
  res = 0
  var = 1
  for i in range(2, len(p), 2):
    if p[(-1) * i] == int(i / 2) and var == 1:
      res = int(i / 2)
    else:
      var = -1
  return res


def ss(i):
  return stack_sort(i, [[1, 2, 3], [1, 3, 2]])

def stab(p):
  #calculates the stability of p
  print(1)

def fact(k):
  if k == 1: return 1
  return k*fact(k-1)

def perm_to_dyck(p):
  #converts a 123-avoiding permutation to a dyck path
  ltrmin = []
  dyck = ""
  ltrmin.append(p[0])
  for j in range(len(p)-p[0]+1):
    dyck = dyck + "1"
  dyck = dyck + "0"
  for k in range(1, len(p)):
    if p[k] < ltrmin[-1]:
      ltrmin.append(p[k])
      for l in range(ltrmin[-2]-p[k]):
        dyck = dyck + "1"
    dyck = dyck + "0"
  return dyck



'''
for k in range(4, 11):
  perms = permutations(list_n(k))
  maximal = []
  s = 0
  for i in perms:
    ord = 0
    temp = i
    while not half_decreasing(temp):
      temp = ss(temp)
      ord += 1
    s += ord
  print(s/fact(k))
'''



  
    #if (ord == k-1 and k % 2 == 1) or (ord == k-2 and k % 2 == 0):
      #print(i)

def leftmost(p):
  #leftmost occurence of 1,2,3
  for i in range(0, len(p)-2):
    for j in range(i+1, len(p)-1):
      for k in range(j+1, len(p)):
        if p[i] < p[j] and p[j] < p[k]:
          return i,j,k
  return -1

def set_avoidance(p , t):
  #check if list of permutations p avoids t
  for i in p:
    if contains(i, t):
      return False
  return True

def h(k):
  #special permutation h for the 132 321 sort
  p = [1]
  for i in range(math.floor(k/2)+2, 1, -1):
    p.append(i)
  return p


def wholess(p, k):
  start = permutations(list_n(p))
  distinct = []
  for i in range(k):
    distinct = []
    for j in start:
      if ss(j) not in distinct:
        distinct.append(ss(j))
    start = distinct
  return start

def checkdyck(d):
  #check if string d represents a valid dyck path
  h = 0
  for i in d:
    if i == '1':
      h += 1
    if i == '0':
      h -= 1
    if h < 0:
      return False
  if h != 0:
    return False
  return True

def containsuupdd(d):
  #check if dyck path d contains the uupdd pattern
  uu = []
  dd = []
  for i in range(0, len(d)-1):
    if d[i] == '1' and d[i+1] == '1':
      uu.append(i)
    elif d[i] == '0' and d[i+1] == '0':
      dd.append(i)
  for a in uu:
    for b in dd:
      if b >= a+4:
        if checkdyck(d[a+2:b]):
          return True
  return False

def containsbad132(p):
  #"bad" 132
  for i in range(0, len(p)-2):
    for j in range(i+1, len(p)-1):
      for k in range(j+1, len(p)):
        if p[j] > p[k] and p[k] > p[i]:
          #condition 1
          val = 0
          for m in range(0, i):
            if p[m] < p[j] and p[m] > p[k]:
              val = 1
          for n in range(j+1, k):
            if p[n] < p[i]:
              val = 1
          if val == 0:
            return True
  return False
      

for i in range(5,9):
  k = permutations(list_n(i))
  for m in k:
    if stack_sort(stack_sort(m, [[1,3,2],[3,2,1]]), [[2,1]]) == list_n(i):
      if contains(m, [1,2,3]) or containsbad132(m):
        print(m)

