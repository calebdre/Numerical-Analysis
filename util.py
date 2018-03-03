import numpy
from math import exp 

def generate_iterations(start, step, end):
	return list(numpy.arange(start,  end, step))

def print_iteration_start(method, func_string_representation, domain_min, domain_max, initial_value, step_size, exact_solution_string_representation):
	print(
		"\n\nRunning {} method on {}, t ∈ [{}, {}], y(0) = {}, h = {}, with exact solution {}"
		.format(method, func_string_representation, str(domain_min), str(domain_max), str(initial_value), str(step_size), exact_solution_string_representation)
	)

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
            "initial_value": [.5],
            "max_error": .01
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
            "initial_value": [-1],
            "max_error": .01
        },
        {
            "example": 3,     #5.5 No. 3.d. pg. 330
            "defining_func": [lambda t, y: (t + 2*(t**3))*(y**3) - t*y],
            "func_string_representation": "y' = (t + 2t^3)y^3 - ty",
            "func_string_template": [lambda t, y: "y' = ({} + 2*{}^3)*{}^3 - {}*{}".format(t,t,y,t,y)],
            "exact_solution_func": [lambda t: (3 + 2*(t**2) + 6*exp(t**2))**(-0.5)],
            "exact_solution_func_string_representation": "y(t) = (3 + 2t^2 + 6e^(t^2))^-0.5",
            "domain_min": 0,
            "domain_max": 2,
            "step_size": .01,
            "initial_value": [round(1/3, 10)]
        },

        {
            "example": 4,   #5.9 No. 3.a. pg. 337
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
            "example": 5,   #5.9 No.1.d. pg. 337
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