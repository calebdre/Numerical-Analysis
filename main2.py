import sys
from math import ceil

from rk4 import rk4
from rk2 import rk2
from ab4 import ab4
from predictor import predictor_corrector
from euler import euler
from motified_euler import modified_euler

from util import print_iteration_start

from solver import generate_example_ivps
from plotting import generate_plot

def main(methods, examples, will_generate_plot, should_plot_solution, plot_type):
	ivps = generate_example_ivps()
	if len(examples) > 0:
		ivps = [i for i in ivps if str(i["example"]) in examples]

	input_to_func_map = {
		"euler":("Euler's", euler, 1),
		"meuler":("Modified Euler's", modified_euler, 2),
		"rk2":("Runge-Kutta 2nd Order", rk2, 2),
		"rk4":("Runge-Kutta 4th Order", rk4, 4),
		"ab4":("Adams-Bashforth 4-Step Explicit", ab4, 4),
		"predictor":("Predictor-Corrector Using Adams-Bashforth 4-Step Explicit and Adams-Moulton 3-Step Implicit", predictor_corrector, 4)
	}


	orders = [input_to_func_map[method][2] for method in methods]
	
	for ivp in ivps:
		func_string = ivp["func_string_representation"]
		template = ivp["func_string_template"][0]

		domain = (ivp["domain_min"], ivp["domain_max"])
		iv = ivp["initial_value"][0]
		step_size = ivp["step_size"]

		f = ivp["defining_func"][0]
		exact_solution_f = ivp["exact_solution_func"][0]
		example_num = ivp["example"]

		iterations_to_plot = []

		for method in methods:
			method_name, func, order = input_to_func_map[method]
			if max(orders) > order:
				step_size = step_size / max(orders)
			print_iteration_start(
				method_name,
				func_string,
				domain[0],
				domain[1],
				iv,
				step_size,
				""
			)
			
			estimate_vals, solution_vals, iter_vals = func(template, f, step_size, domain, iv, exact_solution_f)
			
			if will_generate_plot:
				if plot_type == "error":
					plot_vals = [solu_val - est_val for solu_val, est_val in zip(solution_vals, estimate_vals)]
				else:
					plot_vals = [est_val for est_val in estimate_vals]
				
				iterations_to_plot.append({
					"x": iter_vals, 
					"y": plot_vals, 
					"name": method_name
				})

				if should_plot_solution:
					iterations_to_plot.append({
						"x": iter_vals, 
						"y": solution_vals, 
						"name": method_name + " (solution)"
					})

		if will_generate_plot:
			print("Generating plot...")
			if should_plot_solution:
				title = "Values for Example {} - {}".format(ivp["example"], ivp["func_string_representation"])
			else:
				title = "Errors for Example {} - {}".format(ivp["example"], ivp["func_string_representation"])

			filename = "{}_{}".format("_".join(methods), str(example_num))
			generate_plot(
				title, 
				"Mesh Points", 
				"Method Values", 
				filename,
				*iterations_to_plot,
			)

if __name__ == '__main__':
    print("*** Numerical IVP Solver **")
    args = sys.argv[1:]
    example_args = [i for i in args if i.isnumeric()]
    method_args = [i for i in args if not i.isnumeric()]
    should_plot = False
    should_plot_solution = False
    plot_type = "error" if "values" not in args else "values"

    if len(example_args) > 0:
        if "plot" in args:
            should_plot = True
            if "solution" in args:
                should_plot_solution = True
                plot_type = "values"
            method_args.pop(method_args.index("plot"))
            print("Plotting {} on examples {}".format( ", ".join(method_args), ", ".join(example_args)))
        else:
            print("Running {} on examples {}...".format( ", ".join(method_args), ", ".join(example_args)))    
    else:
        print("Running {} on all examples...".format( ", ".join(method_args)))
    
    main(method_args, example_args, should_plot, should_plot_solution, plot_type)