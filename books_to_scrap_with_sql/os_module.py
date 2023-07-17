import os
try:
    p = os.path.join(os.getcwd(), "saurabh")
    os.mkdir(p)
except:
    print("saurabh dir created")
uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
try:
    for i in uppercase_letters:
        p = os.path.join(r"C:\Users\Dell\PycharmProjects\pythonProject1\saurabh", i)
        os.mkdir(p)
except FileExistsError:
    print("a-z file created")

try:
    for i in uppercase_letters:
        for j in range(1,10):
            p = os.path.join(fr"C:\Users\Dell\PycharmProjects\pythonProject1\saurabh\{i}", str(j))
            os.mkdir(p)
except FileExistsError:
    print("1-9 file created")

try:
    for i in uppercase_letters:
        for j in range(1,10):
            os.chdir(f"C:/Users/Dell/PycharmProjects/pythonProject1/saurabh/{i}/{j}")
            f = open(f"{i}{j}.txt", "x")
            f.close()
except FileExistsError:
    print(".txt file created")
try:
    count=0
    for i in uppercase_letters:
        for j in range(1,10):
            os.chdir(f"C:/Users/Dell/PycharmProjects/pythonProject1/saurabh/{i}/{j}")
            f = open(f"{i}{j}.txt", "w")
            f.write(str(count))
            count +=1
            f.close()
except FileExistsError:
    print("data filled")
try:
    for i in uppercase_letters:
        for j in range(1,10):
            a=f"C:/Users/Dell/PycharmProjects/pythonProject1/saurabh/{i}/{j}"
            l=r"C:/Users/Dell/PycharmProjects/pythonProject1/master"
            n=os.listdir(a)
            for i in n:
                s = os.path.join(a, i)
                d = os.path.join(l, i)
                os.replace(s, d)
except FileNotFoundError:
    print("replace")

