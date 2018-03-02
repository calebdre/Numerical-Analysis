import matplotlib.pyplot as plt
import os

def generate_plot(title, xlabel, ylabel, *pairs):
	colors = ["-r","-g","-b","-c","-y","-m", "-b"]
	# loop twice - once to show and once to save
	for i in range(2): 
		for pair, color in zip(pairs, colors):
			plt.plot(pair["x"], pair["y"], color, label=pair["name"])
			plt.legend(loc='upper left')
		plt.title(title)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)

		if i == 0:
			plt.show()
		else:
			path = "./plot.pdf"
			if os.path.exists(path):
				os.remove(path)
			plt.savefig(path)
	
		