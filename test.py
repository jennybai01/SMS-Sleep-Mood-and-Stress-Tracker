import seaborn as sns
import matplotlib.pyplot as plt

print('Hello, World!')

x = [x for x in range(100)]
y = [y*y for y in range(100)]

ax = sns.lineplot(x=x, y=y)
plt.show()