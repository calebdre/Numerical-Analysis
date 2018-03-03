from math import exp, ceil, sin, cos
from methods import rk2
from copy import deepcopy

def generate_example_ivps():
    return [ # need at least 5
        {
            "example": 1,
            "defining_func": [lambda tau, w: w - (tau**2) + 1.0],
            "func_string_representation": "y' = y - t^2 + 1",
            "func_string_template": [lambda tau, w: "{} - ({})^2 + 1".format(w, tau)],  #template to print the out the individual steps of evaluation
            "exact_solution_func": lambda t: (t+1.0)**2 - exp(t)/2.0,
            "exact_solution_func_string_representation": "y(t) = (t+1)^2 - exp(t)/2",
            "domain_min": 0,
            "domain_max": 2,
            "step_size": .2,
            "initial_value": [.5],
            "max_error": .01
        },
        {
            # Exercise 5.3 No.10 on page 282
            "example": 2,
            "defining_func": [lambda tau, w: 1.0/(tau**2) - w/tau - w**2],
            "func_string_representation": "y' = 1/t^2 - y/t - y^2",
            "func_string_template": [lambda tau, w: "1/{}^2 - {}/{} - {}^2".format(tau, w, tau, w)],
            "exact_solution_func": lambda t: -1.0/t,
            "exact_solution_func_string_representation": "y(t) = -1/t",
            "domain_min": 1,
            "domain_max": 2,
            "step_size": .05,
            "initial_value": [-1],
            "max_error": .01
        },

        {
            "example": 3,
            "defining_func": [
                lambda tau, y, dz: exp(2*tau)*sin(tau) - (2*y) - dz,
                lambda tau, y, z: exp(2*tau)*sin(tau) + z - (2*y)
            ],
            "func_string_representation": "z = dy/dt = e^2t * sin(t) - 2y - dz/dx , dz/dt = e^2t * sin(t) + z - 2y",
            "func_string_template": [
                lambda tau, y, dz: "e^2{} * sin({}) - 2{} - {}".format(tau, tau, y, dz),
                lambda tau, y, z: "e^2{} * sin({}) + {} - 2{}".format(tau, tau, z, y),
            ],
            "exact_solution_func": lambda t: 0.2 * exp(2*t) * (sin(t) - 2 * cos(t)),
            "exact_solution_func_string_representation": "y(t) = 0.2e^2t * (sin(t) − 2 * cos(t))",
            "domain_min": 0,
            "domain_max": 1,
            "step_size": .1,
            "initial_value": [-.4, -.6],
            "max_error": .01
        }
    ]

def print_iteration_start(method, func_string_representation, domain_min, domain_max, initial_value, step_size, exact_solution_string_representation):
    print(
        "\n\nRunning {} method on {}, t ∈ [{}, {}], y(0) = {}, h = {}, with exact solution {}"
        .format(method, func_string_representation, str(domain_min), str(domain_max), str(initial_value), str(step_size), exact_solution_string_representation)
    )

def print_iteration(ti, wi, result, exact_solution):
    print("ti = {}, wi = {}, f(ti, wi) = {}, exact solution: {}, error: {}\n".format(ti, wi, result, 
          round(exact_solution, 10), round((exact_solution - result), 10)))

def calc_exact_solution(example_num):
    ivp = [i for i in generate_example_ivps() if i["example"] == example_num][0]
    iterations = ceil((ivp["domain_max"] - ivp["domain_min"]) / ivp["step_size"])
    iteration_values = [ivp["domain_min"] + round((i * ivp["step_size"]), 10) for i in range(iterations+1)]
    solution = [ivp["exact_solution_func"](val) for val in iteration_values]
    plottable = {"x": iteration_values,"y": solution, "name": "Exact Solution"}
    return plottable

def run_iterations(ivp, method_name, method_func, iteration_values, arg_num):
	step_size = ivp["step_size"]
	defining_funcs = ivp["defining_func"]

	print_iteration_start(
		method_name,
		ivp["func_string_representation"],
		ivp["domain_min"],
		ivp["domain_max"],
		ivp["initial_value"],
		step_size,
		ivp["exact_solution_func_string_representation"]
	)
	
	result = [[i for i in ivp["initial_value"]]]
	exact_solution_results = [*ivp["initial_value"]]
	
	if  arg_num > 1:
		first_iter_values = [iteration_values.pop(0) for i in range(arg_num-1)]
		first_values, first_solutions = run_iterations(ivp, "Runge Kutta Order 2", rk2, first_iter_values, 1)

		result += first_values
		exact_solution_results += first_solutions

	index = len(result)

	for ti in iteration_values:
		exact_val = ivp["exact_solution_func"](ti)
		exact_solution_results.append(exact_val)
		
		prev_ws = result[index - arg_num: index]
		func_vals = []

		for f, template in zip(defining_funcs, ivp["func_string_template"]):
			iter_val = round(method_func(
					f, 
					template,
					step_size, 
					round((ti - step_size), 10), 
					*prev_ws
				), 10)
			
			print_iteration(ti, prev_ws, iter_val, exact_val)
			func_vals.append(iter_val)
		
		result.append(func_vals)
		index += 1
		
	new_results = []
	for num in range(len(defining_funcs)):
		new_results.append([])

	for points in result:
		for i, point in enumerate(points):
			new_results[i].append(point)

	return (new_results, exact_solution_results)
