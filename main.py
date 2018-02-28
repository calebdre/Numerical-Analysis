import sys 
from math import exp, ceil, sin, cos

def higher_order_euler(h, t, funcs, temps prev_values):
    result = []

    for f, w, temp in zip(funcs, ws, temps):
        print("{} + {} * ({})".format(w,h, te(t,prev))
        result.append(euler(h,t,f,w))

    return result

def euler(h, t, temps, funcs, ws):
    """
    f = defining function
    h = step size
    t = prev mesh point (ti - 1)
    w = previous value (wi-1)
    temp = function string template to print out
    """
    result = []

    for f, w, temp in zip(funcs, ws, temps):
        print("{} + {} * ({})".format(w,h, te(t,prev))
        result.append(w + h * func(t, *w))

    return result


def modified_euler(f, temp, h, t, w):
    print("{} + {}/2 * (".format(w,h) + temp(t, w) + " + " + temp(
            t + h, "({} + {}*({}))".format(w, h, temp(t,w))) + ")"
    )
    return w + h/2 * (f(t, w) + f(t + h, w + (h * f(t, w))))


def rk2(f, temp, h, t, w,):
    print("{} + {} * (".format(w,h) + temp("{} + {}/2".format(t,h),
          "{} + {}/2 * ({})".format(w, h, temp(t,w))) + ")")
    return w + h * f(t + h/2, w + h/2 * (f(t, w)))



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


def generate_example_ivps():
    return [ # need at least 5
        {
            "example": 1,
            "defining_func": lambda tau, w: w - (tau**2) + 1.0,
            "func_string_representation": "y' = y - t^2 + 1",
            "func_string_template": lambda tau, w: "{} - ({})^2 + 1".format(w, tau),  #template to print the out the individual steps of evaluation
            "exact_solution_func": lambda t: (t+1.0)**2 - exp(t)/2.0,
            "exact_solution_func_string_representation": "y(t) = (t+1)^2 - exp(t)/2",
            "domain_min": 0,
            "domain_max": 2,
            "step_size": .2,
            "initial_value": .5
        },
        {
            # Exercise 5.3 No.10 on page 282
            "example": 2,
            "defining_func": lambda tau, w: 1.0/(tau**2) - w/tau - w**2,
            "func_string_representation": lamba t,c :"y' = 1/t^2 - y/t - y^2",
            "exact_solution_func": lambda t: -1.0/t,
            "exact_solution_func_string_representation": "y(t) = -1/t",
            "domain_min": 1,
            "domain_max": 2,
            "step_size": .05,
            "initial_value": -1
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
            "exact_solution_func": lambda t: 0.2 * exp(2*t) * (sin(t) − 2 * cos(t)),
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

def main(methods):
    ivps = generate_example_ivps()

    for ivp in ivps:
        iterations = ceil((ivp["domain_max"] - ivp["domain_min"]) / ivp["step_size"])
        iteration_values = [ivp["domain_min"] + round((i * ivp["step_size"]), 10) for i in range(iterations+1)[1:]]
        def run_iterations(method_name, method_func, arg_num):
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
                result = [ivp["initial_value"]]
                index = 1
            elif arg_num == 3:
                result = [iteration_values.pop(0) for i in range(3)]
                index = 3
            
            for ti in iteration_values:
                if arg_num == 1:
                    prev_w = result[index - 1]
                    iter_val = round(method_func(
                            ivp["defining_func"], 
                            ivp["func_string_template"],
                            ivp["step_size"], 
                            round((ti - ivp["step_size"]), 10), 
                            prev_w
                        ), 10)
                    print_iteration(ti, prev_w, iter_val, ivp["exact_solution_func"](ti))
                elif arg_num == 3:
                    iter_val = round(method_func(
                        ivp["defining_func"],
                        ivp["func_string_template"],
                        ivp["step_size"], 
                        round((ti-ivp["step_size"]),10), 
                        result[index - 3],
                        result[index - 2],
                        result[index - 1]
                    ), 10)
                    print_iteration(ti, result[index - 1], iter_val, ivp["exact_solution_func"](ti))
                result.append(iter_val)
                index += 1
            return result
        
        if "all" in methods:
            run_iterations("Euler's", euler, 1)
            run_iterations("Modified Euler's", modified_euler, 1)
            run_iterations("Runge-Kutta 2nd Order", euler, 1)
            run_iterations("Runge-Kutta 4th Order", euler)
            run_iterations("Adams-Bashforth 4-Step Explicit", ab_four_step_explicit, 3)
            run_iterations("Predictor-Corrector Using Adams-Bashforth 4-Step Explicit and Adams-Moulton 3-Step Implicit", predictor_corrector, 3)
            return

        if "euler" in methods:
            run_iterations("Euler's", euler, 1)

        if "modified-euler" in methods:
            run_iterations("Modified Euler's", modified_euler, 1)

        if "rk2" in methods:
            run_iterations("Runge-Kutta 2nd Order", rk2, 1)

        if "rk4" in methods:
            run_iterations("Runge-Kutta 4th Order", rk4, 3)

        if "ab4" in methods:
            run_iterations("Adams-Bashforth 4-Step Explicit", ab_four_step_explicit, 3)
        
        if "predictor" in methods:
            run_iterations("Predictor-Corrector Using Adams-Bashforth 4-Step Explicit and Adams-Moulton 3-Step Implicit", predictor_corrector, 3)
                
if __name__ == '__main__':
    if len(sys.argv) == 1 or "all" in sys.argv:
        methods = ["all"]
        print("*** Numerical IVP Solver **")
    else:
        methods = sys.argv[1:]
        print("Running {}...".format( ", ".join(methods)))
