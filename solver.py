from math import exp, ceil
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
            "example": 3,   #5.9 No. 3.a. pg. 337
            "defining_func": [
                lambda u2: u2,
                lambda t, u1, u2: t*exp(t) - t - u1 + 2*u2
            ],
            "func_string_representation": "y'' - 2y' + y = te^t - t",
            "func_string_template": [
                lambda u2: "y' = {}".format(u2),
                lambda t, u1, u2: "y'' = {}*exp({}) - {} - {} + 2*{}".format(t, t, t, u1, u2)
            ],
            "exact_solution_func": [lambda t: 1/6*(t**3)*exp(t) - t*exp(t) + 2*exp(t) - t - 2],
            "exact_solution_func_string_representation": "y(t) = 1/6*(t^3)*e^t - t*e^t - t - 2",
            "domain_min": 0,
            "domain_max": 1,
            "step_size": .1,
            "initial_value": [0, 0],
            "max_error": .01
        },
        
        {
            "example": 4,   #5.9 No.1.d. pg. 337
            "defining_func": [
                lambda t, u2, u3: u2 - u3 + t,
                lambda t: 3*t**2,
                lambda t, u2: u2 + exp(-t)
            ],
            "func_string_representation": "u1' = u2 - u3 + t, u2' = 3t^2, u3' = u2 + e^-t",
            "func_string_template": [
                lambda t, u2, u3: "{} - {} + {}".format(u2, u3, t),
                lambda t: "3*{}^2".format(t),
                lambda t, u2:"{} + e^(-{})".format(u2, t)
                ],
            "exact_solution_func": [
                lambda t: -0.05*t**5 + 0.25*t**4 + t + 2 - exp(-t),
                lambda t: t**3 + 1,
                lambda t: 0.25*t**4 + t - exp(-t)
            ],
            "exact solution_func_string_representation": "u1(t) = -0.05t^5 + 0.25t^4 + t + 2 - e^-t, u2(t) = t^3 + 1, u3(t) = 0.25t^4 + t - e^-t",
            "domain_min": 0,
            "domain_max": 1,
            "step_size": .1,
            "initial_value": [1, 1, -1],
            "max_error": .001
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
    solutions = [] 
    for f in ivp["exact_solution_func"]:
        solutions.append([f(val) for val in iteration_values])
		
    plottable = [{"x": iteration_values,"y": solution, "name": "Exact Solution"} for solution, i in zip(solutions, range(len(solutions)))]
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
			
			print_iteration(ti, result[index - 1], iter_val, exact_val)

			exact_solution_results.append(exact_val)
			result.append(iter_val)
		index += 1

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
