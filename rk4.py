from math import ceil
from util import generate_iterations

def rk4(template, f, h, bounds, iv, solution_f):
	start, stop = bounds
	iteration_values = generate_iterations(start + h, h, stop+h)
	estimate = [iv]
	solution = [iv]

	for i, t in enumerate(iteration_values, 1):
		w = estimate[i-1]
		
		k1 = f(t-h, w)
		k2 = f(t-h + (h/2), w + (h/2) * k1)
		k3 = f(t-h + (h/2), w + (h/2) * k2)
		k4 = f(t, w + (h*k3))
		
		calc = w + ((h/6) * (k1 + 2*k2 + 2*k3 + k4))
		solu = solution_f(t)
		print("ti = {}, w = {}, h = {}\n{} + {} * {} = {} , exact: {}\n".format(round(t, 6), round(w, 6), round(h, 6), round(w, 6) ,round(h, 6) , template(round(t-h,4),  round(w,4)), round(calc, 4), round(solu, 4)))
				
		estimate.append(calc)
		solution.append(solu)
	
	estimate.pop(0)
	solution.pop(0)

	return estimate, solution, iteration_values