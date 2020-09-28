import matplotlib.pyplot as plt

filename = "Rocket_Booster.txt"
filereader = open(filename, "r")

text = filereader.readlines()
iend = len(text) - 1

x = []
y = []

for i in range(iend):
    x.append(i/300)
    v = text[i].split()
    y.append(float(v[0]))

plt.plot(x,y)
plt.show()
