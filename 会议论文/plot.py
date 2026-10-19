import json
import matplotlib.pyplot as plt
import numpy as np
filename="fc_T_30"
f=open(".\\saves\\{}.json".format(filename))
data=json.load(f)
R = np.arange(0, 1.05, 0.05)
Thre = [10, 50, 100, 200]
colors=['red','green','blue','black']
markers=['o', 's', 'p', '^']
plt.figure(figsize=(8,8))
for i in range(4):
    plt.plot(R,data["{}".format(Thre[i])][0:50],lw=1,marker=markers[i],markersize=10,color=colors[i],label=(Thre[i]))
plt.xlabel("$r$",fontsize=22)
plt.ylabel("$f_c$",fontsize=22)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylim([-0.1,1.1])
plt.legend(fontsize=20,loc='best')
plt.savefig(".\\saves\\{}.pdf".format(filename),dpi=400)
plt.show()