from math import ceil
from .rk4 import rk4
from util import generate_example_ivps, generate_iterations

def ab4(template, f, h, bounds, iv, solution_f):
	start, stop = bounds
	iteration_values = generate_iterations(start+h, h, stop+h)
	saved_iteration_vals = list(iteration_values)

	first_iter_values = [iteration_values.pop(0) for i in range(4)]
	estimate, solution, ignored= rk4(template, f, h, (first_iter_values[0]-h, first_iter_values[-1]), iv, solution_f)
	for i, t in enumerate(iteration_values, 4):
		w1 = estimate[i-1]
		w2 = estimate[i-2]
		w3 = estimate[i-3]
		w4 = estimate[i-4]
		
		f1 = f(t-h, w1)
		f2 = f(t - (h*2), w2)
		f3 = f(t - (3*h), w3)
		f4 = f(t - (4*h), w4)
		
		calc = w1 + h/24 * (55*f1 - 59*f2 + 37*f3 - 9*f4)
		solu = solution_f(t)

		print("\nti = {}\n val: {}, exact: {}, error: {}\n".format(t,round(calc, 5), round(solu,5), round(solu - calc, 5)))
		
		estimate.append(calc)
		solution.append(solu)
	
	estimate.pop(0)
	solution.pop(0)
	saved_iteration_vals.pop(0)

	return estimate, solution, saved_iteration_vals