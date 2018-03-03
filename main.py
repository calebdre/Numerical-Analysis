import sys 
from math import ceil

from methods import predictor_corrector, ab_four_step_explicit, euler, modified_euler, rk2, rk4
from solver import run_iterations, generate_example_ivps, calc_exact_solution
from plotting import generate_plot

def main(methods, examples, will_generate_plot, should_plot_solution, plot_type):
    ivps = generate_example_ivps()
    if len(examples) > 0:
        ivps = [i for i in ivps if str(i["example"]) in examples]
    
    for ivp in ivps:
        iterations = ceil((ivp["domain_max"] - ivp["domain_min"]) / ivp["step_size"])
        iteration_values = [ivp["domain_min"] + round((i * ivp["step_size"]), 10) for i in range(iterations+1)[1:]]
        
        if "all" in methods:
            run_iterations(ivp, "Euler's", euler, iteration_values, 1)
            run_iterations(ivp, "Modified Euler's", modified_euler, iteration_values, 1)
            run_iterations(ivp, "Runge-Kutta 2nd Order", rk2, iteration_values, 1)
            run_iterations(ivp, "Runge-Kutta 4th Order", rk4, iteration_values, 1)
            run_iterations(ivp, "Adams-Bashforth 4-Step Explicit", ab_four_step_explicit, iteration_values, 3)
            run_iterations(ivp, "Predictor-Corrector Using Adams-Bashforth 4-Step Explicit and Adams-Moulton 3-Step Implicit", predictor_corrector, iteration_values, 3)
            return
        
        iterations_to_plot = []
        input_to_func_map = {
            "euler":("Euler's", euler, 1),
            "meuler":("Modified Euler's", modified_euler, 1),
            "rk2":("Runge-Kutta 2nd Order", rk2, 1),
            "rk4":("Runge-Kutta 4th Order", rk4, 3),
            "ab4":("Adams-Bashforth 4-Step Explicit", ab_four_step_explicit, 3),
            "predictor":("Predictor-Corrector Using Adams-Bashforth 4-Step Explicit and Adams-Moulton 3-Step Implicit", predictor_corrector, 3)
        }

        for method in methods:
            if method in input_to_func_map.keys():
                method_name, func, arg_num = input_to_func_map[method]
                result, exact = run_iterations(ivp, method_name, func, iteration_values, arg_num)
                
                if will_generate_plot:
                    if plot_type == "error":
                        plot_vals = [ex - estimate for ex, estimate in zip(exact, result)]
                    else:
                        plot_vals = [estimate for estimate in result]
                    iter_values_with_min = list(iteration_values)
                    iter_values_with_min.insert(0,ivp["domain_min"])

                    iterations_to_plot.append({
                        "x": iter_values_with_min, 
                        "y": plot_vals, 
                        "name": method_name
                    })
        
        if will_generate_plot:
            print("Generating plot...")
            if should_plot_solution:
                iterations_to_plot += calc_exact_solution(ivp["example"])
                title = "Values for Example {} - {}".format(ivp["example"], ivp["func_string_representation"])
            else:
                title = "Errors for Example {} - {}".format(ivp["example"], ivp["func_string_representation"])
            generate_plot(
                title, 
                "Mesh Points", 
                "Method Values", 
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