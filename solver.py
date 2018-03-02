from math import exp, ceil, sin, cos

def generate_example_ivps():
    return [ # need at least 5
        {
            "example": 1,
            "defining_func": [lambda tau, w: w - (tau**2) + 1.0],
            "func_string_representation": "y' = y - t^2 + 1",
            "func_string_template": [lambda tau, w: "{} - ({})^2 + 1".format(w, tau)],  #template to print the out the individual steps of evaluation
            "exact_solution_func": [lambda t: (t+1.0)**2 - exp(t)/2.0],
            "exact_solution_func_string_representation": "y(t) = (t+1)^2 - exp(t)/2",
            "domain_min": 0,
            "domain_max": 2,
            "step_size": .2,
            "initial_value": [.5]
        },
        {
            # Exercise 5.3 No.10 on page 282
            "example": 2,
            "defining_func": [lambda tau, w: 1.0/(tau**2) - w/tau - w**2],
            "func_string_representation": "y' = 1/t^2 - y/t - y^2",
            "func_string_template": [lambda tau, w: "1/{}^2 - {}/{} - {}^2".format(tau, w, tau, w)],
            "exact_solution_func": [lambda t: -1.0/t],
            "exact_solution_func_string_representation": "y(t) = -1/t",
            "domain_min": 1,
            "domain_max": 2,
            "step_size": .05,
            "initial_value": [-1]
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
            "exact_solution_func": [lambda t: 0.2 * exp(2*t) * (sin(t) - 2 * cos(t))],
            "exact_solution_func_string_representation": "y(t) = 0.2e^2t * (sin(t) − 2 * cos(t))",
            "domain_min": 0,
            "domain_max": 1,
            "step_size": .1,
            "initial_value": [-.4, -.6]
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
    return plottable

def run_iterations(ivp, method_name, method_func, iteration_values, arg_num):
	print_iteration_start(
		method_name,
		ivp["func_string_representation"],
		ivp["domain_min"],
		ivp["domain_max"],
		ivp["initial_value"],
		ivp["step_size"],
		ivp["exact_solution_func_string_representation"]
	)

	if arg_num == 1:
		result = [i for i in ivp["initial_value"]]
	elif arg_num == 3:
		result = [iteration_values.pop(0) for i in range(3)]
	
	exact_solution_results = list(result)
	index = len(result)

	for ti in iteration_values:
		if arg_num == 1:
			defining_funcs = ivp["defining_func"]
			prev_ws = result[index - len(defining_funcs): index]
			for f, template, exact_solution in zip(defining_funcs, ivp["func_string_template"], ivp["exact_solution_func"]):
				exact_val = exact_solution(ti)
				iter_val = round(method_func(
						f, 
						template,
						ivp["step_size"], 
						round((ti - ivp["step_size"]), 10), 
						prev_ws
					), 10)
				
				print_iteration(ti, prev_ws, iter_val, exact_val)
				
				exact_solution_results.append(exact_val)
				result.append(iter_val)
		elif arg_num == 4:
			exact_val = ivp["exact_solution_func"](ti)
			iter_val = round(method_func(
				ivp["defining_func"],
				ivp["func_string_template"],
				ivp["step_size"], 
				round((ti-ivp["step_size"]),10), 
            result[index - 1],
				result[index - 2],
				result[index - 3],
				result[index - 4]
			), 10)
			
			print_iteration(ti, result[index - 1], iter_val, exact_val)

			exact_solution_results.append(exact_val)
			result.append(iter_val)
		index += 1
	return (result, exact_solution_results)