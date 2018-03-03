from math import ceil
from util import generate_iterations

def rk4(template, f, h, bounds, iv, solution_f):
	start, stop = bounds
	iteration_values = generate_iterations(start, h, stop)
	estimate = [iv]
	solution = [iv]

	for i, t in enumerate(iteration_values):
		w = estimate[i-1]
		
		k1 = f(t, w)
		k2 = f(t + (h/2), w + (h/2) * k1)
		k3 = f(t + (h/2), w + (h/2) * k2)
		k4 = f(t + h, w + (h*k3))
		
		# print("k1 = {} = {}".format(template(t,w), k1))
		# print("k2 = {} = {}".format(template("{} + {}/2".format(t,h), "{} + {}/2 * {}". format(w, h, k1)), k2))
		# print("k3 = {} = {}".format(template("{} + {}/2".format(t,h), "{} + {}/2 * {}". format(w, h, k2)), k3))
		# print("k4 = {} = {}".format(template("{} + {}".format(t,h), "{} + {}*{}". format(w, h, k3)), k4))
		# print("{} + {}/6 * ({} + 2*{} + 2*{} + {})".format(w, h, k1, k2, k3, k4))
		
		estimate.append(w + ((h/6) * (k1 + 2*k2 + 2*k3 + k4)))
		solution.append(solution_f(t))
	
	estimate.pop(0)
	solution.pop(0)

	return estimate, solution, iteration_values