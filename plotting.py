import matplotlib.pyplot as plt

def generate_plot(title, xlabel, ylabel, *pairs):
    colors = ["-r","-g","-b","-c","-y","-m", "-b"]
    for pair, color in zip(pairs, colors):
        plt.plot(pair["x"], pair["y"], color, label=pair["name"])
        plt.legend(loc='upper left')

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()