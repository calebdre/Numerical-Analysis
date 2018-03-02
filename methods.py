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