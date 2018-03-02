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
    
    return w1 + h/24 * (55 * f1 - 59 * f2 + 37 * f3 - 9 * f4)
    


def predictor_corrector(f, temp, h, t, w1, w2, w3, w4):
    """
    Uses Adams-Bashforth 4-step explicit method as the predictor and 
    Adams-Moulton 3-step implicit method as the corrector.
    """
    w_p = ab_four_step_explicit(f, temp, h, t, w1, w2, w3, w4)
    f1 = f(t, w1)
    f2 = f(t - h, w2)
    f3 = f(t - 2*h, w3)
    
    return w1 + h/24 * (9 * w_p + 19 * f1 - 5 *f2 + f3)

def adaptive_rk4(f, temp, h, t, w):
    
    raise Exception("Not Implemented")

def adaptive_pc(f, temp, h, t, w1, w2, w3, w4):
    
    raise Exception("Not Implemented")
    

    