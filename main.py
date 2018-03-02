import sys 
from math import exp, ceil, sin, cos
import matplotlib.pyplot as plt


#https://plot.ly/python/getting-started/

def euler(f, temp, h, t, ws):
    """
    f = defining function
    h = step size
    t = prev mesh point (ti - 1)
    w = previous value (wi-1)
    temp = function string template to print out
    """

    print("{} + {} * ({})".format(ws[0], h, temp(t,*ws)))
    return ws[0] + (h * f(t, *ws))


def modified_euler(f, temp, h, t, w):
    # print("{} + {}/2 * ({})".format(w[0],h) + temp(t, *w) + " + " + temp(
    #         t + h, "({} + {}*({}))".format(w[0], h, temp(t,*w))) + ")"
    # )
    return w[0] + h/2 * (f(t, *w) + f(t + h, w[0] + (h * f(t, *w)), *w[1:]))


def rk2(f, temp, h, t, w):
    print("{} + {} * ({})".format(w[0],h, temp(t, *w)),
          "{} + {}/2 * ({})".format(w[0], h, temp(t,*w)))

    return w[0] + h * f(t + h/2, w[0] + (h/2 * f(t, *w)), *w[1:])



def rk4(f, temp, h, t, w1, w2, w3):
    raise Exception("Not Implemented")


def ab_four_step_explicit(f, temp, h, t, w1, w2, w3):
    raise Exception("Not Implemented")


def predictor_corrector(f, temp, h, t, w1, w2, w3):
    """
    Uses Adams-Bashforth 4-step explicit method as the predictor and 
    Adams-Moulton 3-step implicit method as the corrector.
    """

    raise Exception("Not Implemented")

def generate_plot(title, xlabel, ylabel, *pairs):
    colors = ["-r","-g","-b","-c","-y","-m", "-b"]
    for pair, color in zip(pairs, colors):
        print(pair)
        plt.plot(pair["x"], pair["y"], color, label=pair["name"])
        plt.legend(loc='upper left')

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

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

def main(methods, examples, will_generate_plot, should_plot_solution, plot_type):
    ivps = generate_example_ivps()
    if len(examples) > 0:
        ivps = [i for i in ivps if str(i["example"]) in examples]

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
                elif arg_num == 3:
                    exact_val = ivp["exact_solution_func"](ti)
                    iter_val = round(method_func(
                        ivp["defining_func"],
                        ivp["func_string_template"],
                        ivp["step_size"], 
                        round((ti-ivp["step_size"]),10), 
                        result[index - 3],
                        result[index - 2],
                        result[index - 1]
                    ), 10)
                    
                    print_iteration(ti, result[index - 1], iter_val, exact_val)

                    exact_solution_results.append(exact_val)
                    result.append(iter_val)
                index += 1
            return (result, exact_solution_results)
    
    for ivp in ivps:
        iterations = ceil((ivp["domain_max"] - ivp["domain_min"]) / ivp["step_size"])
        iteration_values = [ivp["domain_min"] + round((i * ivp["step_size"]), 10) for i in range(iterations+1)[1:]]
        
        if "all" in methods:
            run_iterations(ivp, "Euler's", euler, iteration_values, 1)
            run_iterations(ivp, "Modified Euler's", modified_euler, iteration_values, 1)
            run_iterations(ivp, "Runge-Kutta 2nd Order", euler, iteration_values, 1)
            run_iterations(ivp, "Runge-Kutta 4th Order", euler, iteration_values)
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
                iterations_to_plot += calc_solution(ivp["example"])
                title = "Values for Example {} - {}".format(ivp["example"], ivp["func_string_representation"])
            else:
                title = "Errors for Example {} - {}".format(ivp["example"], ivp["func_string_representation"])
            generate_plot(
                title, 
                "Mesh Points", 
                "Method Values", 
                *iterations_to_plot
            )

def calc_solution(example_num):
    ivp = [i for i in generate_example_ivps() if i["example"] == example_num][0]
    iterations = ceil((ivp["domain_max"] - ivp["domain_min"]) / ivp["step_size"])
    iteration_values = [ivp["domain_min"] + round((i * ivp["step_size"]), 10) for i in range(iterations+1)]
    solutions = [] 
    for f in ivp["exact_solution_func"]:
        solutions.append([f(val) for val in iteration_values])
    
    plottable = [{"x": iteration_values,"y": solution, "name": "Exact Solution"} for solution, i in zip(solutions, range(len(solutions)))]
    return plottable

if __name__ == '__main__':
    if len(sys.argv) == 1 or "all" in sys.argv:
        methods = ["all"]
        print("*** Numerical IVP Solver **")
    else:
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
                method_args.pop(method_args.index("plot"))
                print("Plotting {} on examples {}".format( ", ".join(method_args), ", ".join(example_args)))
            else:
                print("Running {} on examples {}...".format( ", ".join(method_args), ", ".join(example_args)))    
        else:
            print("Running {} on all examples...".format( ", ".join(method_args)))
        
        main(method_args, example_args, should_plot, should_plot_solution, plot_type)
