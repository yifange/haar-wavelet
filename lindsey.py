import numpy as np
import time
from scidbpy import interface, SciDBQueryError, SciDBArray
sdb = interface.SciDBShimInterface('http://localhost:8080')

n = 8
chunk = 8
img_array = np.around(np.random.rand(n,n) * 255,0)
img = sdb.from_array(img_array, persistent=False, chunk_size=chunk)

start = time.time()

#### Splitting #####

if "a" in sdb.list_arrays():
  sdb.query("remove(a)")
if "b" in sdb.list_arrays():
  sdb.query("remove(b)")
if "c" in sdb.list_arrays():
  sdb.query("remove(c)")
if "d" in sdb.list_arrays():
  sdb.query("remove(d)")

sdb.query('store(thin({A}, 0,2,0,2), a)', A=img)
sdb.query('store(thin({A}, 0,2,1,2), b)', A=img)
sdb.query('store(thin({A}, 1,2,0,2), c)', A=img)
sdb.query('store(thin({A}, 1,2,1,2), d)', A=img)

sdb.query('store(a / 2,a)')


"""
a = sdb.new_array((n/2,n/2), persistent=False, chunk_size=chunk/2, dtype='double')
b = sdb.new_array((n/2,n/2), persistent=False, chunk_size=chunk/2, dtype='double')
c = sdb.new_array((n/2,n/2), persistent=False, chunk_size=chunk/2, dtype='double')
d = sdb.new_array((n/2,n/2), persistent=False, chunk_size=chunk/2, dtype='double')

sdb.query('store(thin({A}, 0,2,0,2),{B})', A=img, B=a)
sdb.query('store(thin({A}, 0,2,1,2),{B})', A=img, B=b)
sdb.query('store(thin({A}, 1,2,0,2),{B})', A=img, B=c)
sdb.query('store(thin({A}, 1,2,1,2),{B})', A=img, B=d)

last = time.time()
print "splitting: ", time.time() - start
start = last 

# Predict and update (single level)
a = (a + b + c + d) / 2 # 4 cell average * 2
b = b + d - a           # upper right detail
c = c + d - a           # lower left detail
d = 2*d - (a + b + c)   # lower right detail

# Create compressed matrix
#e = a/2
#print e.toarray()

# Get decompressed matrix
d = (a + b + c + d) / 2
c = c + a - d
b = b + a - d
a = 2*a - (b + c + d)

last = time.time()
print "arithmetic: ", time.time() - start
start = last 

# Put it all into a single matrix
anew = sdb.new_array((n,n), persistent=False, chunk_size=chunk, dtype='double')
bnew = sdb.new_array((n,n), persistent=False, chunk_size=chunk, dtype='double')
cnew = sdb.new_array((n,n), persistent=False, chunk_size=chunk, dtype='double')
dnew = sdb.new_array((n,n), persistent=False, chunk_size=chunk, dtype='double')

sdb.query('store(xgrid({A},2,2),{B})', A=a, B=anew)
sdb.query('store(xgrid({A},2,2),{B})', A=b, B=bnew)
sdb.query('store(xgrid({A},2,2),{B})', A=c, B=cnew)
sdb.query('store(xgrid({A},2,2),{B})', A=d, B=dnew)

last = time.time()
print "big grids: ", time.time() - start
start = last 

sdb.query('store(filter({A}, abs({A.d0}) % 2 = 0 and abs({A.d1}) % 2 = 0), {A})', A=anew)
sdb.query('store(filter({A}, abs({A.d0}) % 2 = 0 and abs({A.d1}) % 2 = 1), {A})', A=bnew)
sdb.query('store(filter({A}, abs({A.d0}) % 2 = 1 and abs({A.d1}) % 2 = 0), {A})', A=cnew)
sdb.query('store(filter({A}, abs({A.d0}) % 2 = 1 and abs({A.d1}) % 2 = 1), {A})', A=dnew)

last = time.time()
print "filters: ", time.time() - start
start = last 

sdb.query('insert({A},{B})',A=bnew, B=anew)
sdb.query('insert({A},{B})',A=cnew, B=anew)
sdb.query('insert({A},{B})',A=dnew, B=anew)

last = time.time()
print "inserts: ", time.time() - start
start = last 

print "in: "
print img.toarray()
print "out: "
print anew.toarray()
"""
