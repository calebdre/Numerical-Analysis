import matplotlib.pyplot as plt
import matplotlib
import os

def generate_plot(title, xlabel, ylabel, filename, *pairs):
	colors = ["-r","-g","-b","-c","-y","-m", "-b"]
	
	fig = plt.figure()
	ax = plt.subplot(111)
	ax.set_position([0.1,0.1,0.5,0.8])

	for pair, color in zip(pairs, colors):
		ax.plot(pair["x"], pair["y"], color, label=pair["name"])
	
	ax.set_title(title)
	ax.legend(loc = 'center left', bbox_to_anchor = (1.0, 0.5), labelspacing=1)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)

	path = "./{}.pdf".format(filename)
	if os.path.exists(path):
		os.remove(path)
	plt.savefig(path)
	
		