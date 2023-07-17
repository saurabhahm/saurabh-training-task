l1 = []
n = int(input("enter size of arr"))
for i in range(n):
    x = int(input("enter a number"))
    l1.append(x)

def bin_search(k,l,h, l1):
    if l <= h:
        m = (l + h) // 2
        if l1[m] == k:
            return m
        elif l1[m] > k:
            return bin_search(k, l, m - 1, l1)
        else:
            return bin_search(k,  m+1,h, l1)
    else:
     return -1


for i in range(len(l1)):
    m = i
    for j in range(i + 1, len(l1)):
        if l1[j] < l1[m]:
            m = j
    l1[i], l1[m] = l1[m], l1[i]
k = int(input("enter a number for key"))
l=0
h=len(l1)-1
if bin_search(k, l,h,l1)==-1:
    print("not found")
else:
    print(f"found at {bin_search(k,l,h, l1)} index")


