from math import ceil
from util import generate_iterations

def rk2(template, f, h, bounds, iv, solution_f):
	start, stop = bounds
	iteration_values = generate_iterations(start+h, h, stop+h)
	estimate = [iv]
	solution = [iv]

	for i, t in enumerate(iteration_values, 1):
		w = estimate[i-1]
		calc = w + h * f(t-h + (h/2), w + ((h/2) * f(t-h, w)))
		solu = solution_f(t)

		print("ti = {} , val: {}, exact: {}, error: {}".format(t, round(calc, 5), round(solu,5), round(solu - calc, 5)))
		
		estimate.append(calc)
		solution.append(solu)
	
	estimate.pop(0)
	solution.pop(0)

	return estimate, solution, iteration_values