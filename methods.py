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
  #  print("{} + {}/2 * ({} + {})".format(w[0],h, temp(t,*w), 
  #        temp(t + h, "({} + {}*({}))".format(w[0], h, temp(t,*w))))
  #  )
    return w[0] + h/2 * (f(t, *w) + f(t + h, w[0] + (h * f(t, *w)), *w[1:]))


def rk2(f, temp, h, t, w):
  #  print("{} + {} * ({})".format(w[0],h, temp(t, *w)),
  #       "{} + {}/2 * ({})".format(w[0], h, temp(t,*w)))

    return w[0] + h * f(t + h/2, w[0] + (h/2 * f(t, *w)), *w[1:])



def rk4(f, temp, h, t, w):
    k1 = f(t, w)
    k2 = f(t + h/2, w + h/2 * k1)
    k3 = f(t + h/2, w + h/2 * k2)
    k4 = f(t+h, w + h*k3)
    
    return w + h/6 *(k1 + 2*k2 + 2*k3 + k4)


def ab_four_step_explicit(f, temp, h, t, w1, w2, w3, w4):
    f1 = f(t, w1)
    f2 = f(t - h, w2)
    f3 = f(t - 2*h, w3)
    f4 = f(t - 3*h, w4)
    
    return w1 + h/24 * (55*f1 - 59*f2 + 37*f3 - 9*f4)



def predictor_corrector(f, temp, h, t, w1, w2, w3, w4):
    """
    Uses Adams-Bashforth 4-step explicit method as the predictor and 
    Adams-Moulton 3-step implicit method as the corrector.
    """
    f1 = f(t, w1)
    f2 = f(t - h, w2)
    f3 = f(t - 2*h, w3)
    f4 = f(t - 3*h, w4)
    
    w_p = w1 + h/24 * (55*f1 - 59*f2 + 37*f3 - 9*f4)
    
    return w1 + h/24 * (9*w_p + 19*f1 - 5*f2 + f3)

def adaptive_rk4(f, temp, h, t, w, e):
    """
    Uses Runge-Kutta-Fehlberg method of order 5 and Runge Kutta method of
    order four to control the error e. Returns the array consisting of
    the calculated value and q, the scaling factor of h, to see if the value 
    is valid and if not by how much it has to be scaled.
    Round is used to control the floating point errors. 
    """
    k1 = h*f(t, w)
    k2 = h*f(t + round(1/4, 10)*h, w + round(1/4, 10)*k1)
    k3 = h*f(t + round(3/8, 10)*h, w + round(3/32, 10)*k1 + round(9/32,10)*k2)
    k4 = h*f(t + round(12/13, 10)*h, w + round(1932/2197, 10)*k1 -
             round(7200/2197,10)*k2 + round(7296/2197, 10)*k3)
    k5 = h*f(t + h, w + round(439/216, 10)*k1 - 8*k2 + round(3680/513, 10)*k3 -
             round(845/4104, 10)*k4)
    k6 = h*f(t + h/2, - round(8/27, 10)*k1 + 2*k2 - round(3544/2565, 10)*k3 +
             round(1859/4104, 10)*k4 - round(11/40, 10)*k5)
    w_e4 = (w + round(25/216, 10)*k1 + round(1408/2565, 10)*k3 + 
            round(2197/4104, 10) * k4 - k5/5)
    w_e5 = (w + round(16/135, 10)*k1 + round(6656/12825, 10)*k3 +
            round(28561/56430, 10)*k4 - round(9/50, 10)*k5 + round(2/55, 10)*k6)
    
    q = 0.84*(e*h/abs(w_e5 - w_e4))**(0.25)
    
    return [w_e4, q]
    

def adaptive_pc(f, temp, h, t, w1, w2, w3, w4, e):
    
    raise Exception("Not Implemented")
    

    