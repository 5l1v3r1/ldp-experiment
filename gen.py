import numpy as np
from scipy.linalg import hadamard
import hashlib
import hmac
import re
import pandas as pd
k=8192
epsilon=2
d=50
m=256
cohort=16

def mymd5(s):
    m2 = hashlib.md5()   
    m2.update(s.encode("utf-8"))   
    a=m2.hexdigest()
    a=int(a[0:3],16)%cohort
    return a
    
def sha8192(s):
    s=s.encode("utf-8")
    shaval=""
    for i in range(0,int((k/64)*(3/2))):
        shaval+=hmac.new(str(i).encode("utf-8"),s,hashlib.sha512).hexdigest()
    return np.array([int(i,16)%m for i in re.findall("...",shaval)])



def encode(s,id,orig):
    base=id*8192/cohort
    p=np.exp(epsilon/2)/(np.exp(epsilon/2)+1)
    a=np.zeros(m)
    digest=sha8192(s)
    j=np.random.randint(base,base+8192/cohort)
    a[digest[j]]=1

    hM=hadamard(m)
    w=hM @ a
    l=int(np.random.rand()*m-0.1)
    r=np.random.rand()
    if(r>0 and r<=p):
        pass
    elif(r > p):
        w[l]*=-1
    return np.array([w[l],j,l,orig]).astype(int).astype(str)

def main():
    users=cohort
    n_per_user=int(100000/users)
    for c in range(0,10):
        for user in range(0,users):
            groupid=mymd5(str(user))
            for i in range(0,n_per_user):
                r=int(np.random.rand()*(d-0.1))+1
                msg="[em_"+str(r)+"]"
                encoded=",".join(encode(msg,groupid,r))
                with open("result_"+str(c)+".txt","a+") as f:
                    f.write(encoded+"\n")

if __name__ == "__main__":
    main()
