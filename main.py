import sys 

def euler(h, i, w):
    return 0


def modified_euler(h, i, w):
    return 0


def rk2(h, i, w):
    return 0


def rk4(h, i, w1, w2, w3):
    return 0


def ab_four_step_explicit(h, i, w1, w2, w3):
    return 0


def predictor_corrector(h, i, w1, w2, w3):
    """
    Uses Adams-Bashforth 4-step explicit method as the predictor and 
    Adams-Moulton 3-step implicit method as the corrector.
    """

    return 0


def generate_example_ivps():
    return [ # need at least 5
        {
            # sample data for now
            "func": 0,
            "func_string_representation": "y' = f(x)"
            "domain_min": 0,
            "domain_max": 0,
            "step_size": .1,
            "initial_value": 0
        }
    ]

def print_iteration_start(method, func_string_representation, domain_min, domain_max, initial_value, step_size):
    print(
        "\n\nRunning {} method on {} from {} to {} with initial value y(0) = {} and h = {}"
        .format(method, func_string_representation, str(domain_min), str(domain_max), str(initial_value), str(step_size))
    )

def print_iteration(ti, wi, result):
    print("ti = {}, wi = {}, f(ti, wi) = {}\n".format(ti, wi, result))

def main(methods):
    ivps = generate_example_ivps()

    for ivp in ivps:
        iterations = (ivp.domain_max - ivp.domain_max) / ivp.step_size
        iteration_values = [i * step_size for i in range(iterations)]

        def run_iterations(method_name, method_func, arg_num):
            print_iteration_start(
                method_name,
                ivp.func_string_representation,
                ivp.domain_min,
                ivp.domain_max,
                ivp.initial_value,
                ivp.step_size
            )
 
            if arg_num == 1:
                result = [ivp.initial_value]
                index = 1
            elif arg_num == 3:
                result = [iteration_values.pop(0) for i in range(3)]
                index = 2
            
            for ti in enumerate(iteration_values):
                if arg_num == 1:
                    prev = result[index - 1]
                    iter_val = method_func(ivp.step_size, ti, prev)
                    print_iteration(ti, prev ,iter_val)
                elif arg_num == 3:
                    iter_val = method_func(
                        ivp.step_size, 
                        ti, 
                        result[index - 3],
                        result[index - 2],
                        result[index - 1]
                    )
                    print_iteration(ti, result[index - 1], iter_val)

                result.append(iter_val)
                index += 1
            return result
        
        if "all" in methods:
            run_iterations("Euler's", euler, 1)
            run_iterations("Modified Euler's", modified_euler, 1)
            run_iterations("Runge-Kutta 2nd Order", reuler, 1)
            run_iterations("Runge-Kutta 4th Order", euler)
            run_iterations("Adams-Bashforth 4-Step Explicit", ab_four_step_explicit, 3)
            run_iterations("Predictor-Corrector Using Adams-Bashforth 4-Step Explicit and Adams-Moulton 3-Step Implicit", predictor_corrector, 3)
            return

        if method == "euler":
            run_iterations("Euler's", euler, 1)

        if method == "modified-euler":
            run_iterations("Modified Euler's", modified_euler, 1)

        if method == "rk2":
            run_iterations("Runge-Kutta 2nd Order", reuler, 1)

        if method == "rk4":
            run_iterations("Runge-Kutta 4th Order", euler)

        if method == "ab4":
            run_iterations("Adams-Bashforth 4-Step Explicit", ab_four_step_explicit, 3)
        
        if method == "predictor"
            run_iterations("Predictor-Corrector Using Adams-Bashforth 4-Step Explicit and Adams-Moulton 3-Step Implicit", predictor_corrector, 3)
                
if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[2] == "all":
        methods = ["all"]
        print("*** Numerical IVP Solver **")
    else:
        methods = sys.argv[1:]
        print("Running {}...".format( ", ".join(methods))

    main(methods)

