from math import ceil
from util import generate_iterations

def euler(template, f, h, bounds, iv, solution_f):
	start, stop = bounds
	iteration_values = generate_iterations(start+h, h, stop+h)
	estimate = [iv]
	solution = [iv]

	for i, t in enumerate(iteration_values, 1):		
		w = estimate[i-1]
		calc = w + (h * f(t-h, w))
		solu = solution_f(t)
		# print("val: {}, exact: {}, error: {}".format(round(calc, 5), round(solu,5), round(solu - calc, 5)))
		print("ti = {}, w = {}, h = {}\n{} + {} * {} = {} , exact: {}\n".format(t, w, h, w ,h , template(round(t-h,4),  round(w,4)), round(calc, 4), round(solu, 4)))
		
		estimate.append(calc)
		solution.append(solu)
	
	estimate.pop(0)
	solution.pop(0)

	return estimate, solution, iteration_values