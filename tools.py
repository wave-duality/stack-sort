import itertools

def order_isomorphic(a, b):
  #check whether or not two permutations a and b are order isomorphic
  n = len(a)
  for i in range(0, n-1):
    for j in range(i+1, n):
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
  x = list(set(list(itertools.combinations(t[:-1] , k-1))))
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
  while (len(res)+len(stack) != len(p)):
    avoiding = True
    if (len(stack) == 0):
      stack.append(p[index])
      index += 1
    else:
      stack.append(p[index]) #create hypothetical new stack, check if it contains anything in T4
      for t in T:
        for i in aligned_subsequences(len(t), stack):
          if (order_isomorphic(t[::-1], i)): #reverse everything in t since using list to store stack inherently makes reading go bottom up
            avoiding = False
      if (avoiding == True):
        index += 1 #no issues, move on
      if (avoiding == False):
        stack.pop() #remove hypothetical element
        k = stack.pop() #append original top to res
        res.append(k)
        #don't increase index, since we are still on the same element
    #print(res, stack)
  while (len(stack) > 0):
    k = stack.pop()
    res.append(k)
  return res

def machine(p, sigma, tau):
  #perform the (sigma, tau)-machine on permutation p
  return stack_sort(stack_sort(p, [sigma, tau]), [[2,1]])

def s(p):
  return stack_sort(p, [[2,1]]) #normal sort

def list_n(n):
  return [i for i in range(1, n+1)]

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
    new.append(len(p)+1-i)
  return new

def half_increasing(p):
  return half_decreasing(comp(p))

def half_decreasing(p):
  index = 1
  for j in range(len(p)-2, 0, -2):
    if p[j] != index:
      return False
    index += 1
  return True
