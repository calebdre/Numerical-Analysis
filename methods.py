def euler(f, temp, h, t, ws):
	"""
	f = defining function
	h = step size
	t = prev mesh point (ti - 1)
	w = previous value (wi-1)
	temp = function string template to print out
	"""
	print("{} + {} * ({})".format(ws[0], h, temp(t, *ws)))
	return ws[0] + (h * f(t, *ws))

def modified_euler(f, temp, h, t, w):
    print("{} + {}/2 * ({} + {})".format(w[0],h, temp(t,*w), 
          temp(t + h, "({} + {}*({}))".format(w[0], h, temp(t,*w))))
    )
    return w[0] + h/2 * (f(t, *w) + f(t + h, w[0] + (h * f(t, *w)), *w[1:]))


def rk2(f, temp, h, t, w):
    print("{} + {} * ({})".format(w[0],h, temp(t + h/2, 
         "{} + {}/2 * ({})".format(w[0], h, temp(t,*w))))
    )
    
    return w[0] + h * f(t + h/2, w[0] + (h/2 * f(t, *w)), *w[1:])
    


# def rk4(f, temp, h, t, ws):
# 	print("TSDM", t)
# 	k1s = []
# 	k2s = []
# 	k3s = []
# 	k4s = []

# 	for i, w in enumerate(ws):
# 		k1s.append(w)
# 		k2s.append(w + k1s[i]/2)
# 		k3s.append(w + k2s[i]/2)
# 		k4s.append(w + k3s[i])

# 	k1 = f(t, *k1s)
# 	k2 = f(t + (h/2), *k2s)
# 	k3 = f(t + (h/2), *k3s)
# 	k4 = f(t + h, *k4s)

# 	print("k1 = {} = {}".format(temp(t,*ws), k1))
# 	print("k2 = {} = {}".format(temp("{} + {}/2".format(t,h), "{} + {}/2 * {}". format(*ws, h, k1)), k2))
# 	print("k3 = {} = {}".format(temp("{} + {}/2".format(t,h), "{} + {}/2 * {}". format(*ws, h, k2)), k3))
# 	print("k4 = {} = {}".format(temp("{} + {}".format(t,h), "{} + {}*{}". format(*ws, h, k3)), k4))
# 	print("{} + {}/6 * ({} + 2*{} + 2*{} + {})".format(*ws, h, k1, k2, k3, k4))

# 	return ws[0] + (h/6) * (k1 + (2*k2) + (2*k3) + k4)

def rk4(f, temp, h, t, ws):
    k1 = []
    k2 = []
    k3 = []
    k4 = []
    i = 0
    for w in ws: 
        k1.append(f(t, w))
        k2.append(f(t + h/2, w + h/2 * k1[i]))
        k3.append(f(t + h/2, w + h/2 * k2[i]))
        k4.append(f(t + h, w + h*k3[i]))
        i = i + 1
    
    print("k1 = {} = {}".format(temp(t,*ws), *k1))
    print("k2 = {} = {}".format(temp("{} + {}/2".format(t,h), "{} + {}/2 * {}". format(*ws, h, k1)), *k2))
    print("k3 = {} = {}".format(temp("{} + {}/2".format(t,h), "{} + {}/2 * {}". format(*ws, h, k2)), *k3))
    print("k4 = {} = {}".format(temp("{} + {}".format(t,h), "{} + {}*{}". format(*ws, h, k3)), *k4))
    print("{} + {}/6 * ({} + 2*{} + 2*{} + {})".format(*ws, h, *k1, *k2, *k3, *k4))
    
    return ws[0] + h/6 *(k1[0] + 2*k2[0] + 2*k3[0] + k4[0])

def ab_four_step_explicit(f, temp, h, t, w4, w3, w2, w1):
    f1 = f(t, w1)
    f2 = f(t - h, w2)
    f3 = f(t - 2*h, w3)
    f4 = f(t - 3*h, w4)
    
    print("f(t_i,w_i) = {}".format(temp(t, w1)))
    print("f(t_(i-1),w_(i-1)) = {}".format(temp(t - h, w2)))
    print("f(t_i,w_i) = {}".format(temp(t - 2*h, w3)))
    print("f(t_i,w_i) = {}".format(temp(t - 3*h, w4)))
    print("{} + {}/24 * (55*{} -59*{} + 37*{} - 9*{})".format(w1, h, f1, f2, f3, f4))
    
    
    return w1 + h/24 * (55*f1 - 59*f2 + 37*f3 - 9*f4)



def predictor_corrector(f, temp, h, t, w4, w3, w2, w1):
    """
    Uses Adams-Bashforth 4-step explicit method as the predictor and 
    Adams-Moulton 3-step implicit method as the corrector.
    """
    f1 = f(t, *w1)
    f2 = f(t - h, *w2)
    f3 = f(t - 2*h, *w3)
    f4 = f(t - 3*h, *w4)
    
    w_p = w1[0] + (h/24) * (55*f1 - 59*f2 + 37*f3 - 9*f4)
    
    print("f(t_i,w_i) = {}".format(temp(t, *w1)))
    print("f(t_(i-1),w_(i-1)) = {}".format(temp(t - h, *w2)))
    print("f(t_i,w_i) = {}".format(temp(t - 2*h, *w3)))
    print("f(t_i,w_i) = {}".format(temp(t - 3*h, *w4)))
    print("w_p = {} + {}/24 * (55*{} -59*{} + 37*{} - 9*{})".format(w1[0], h, f1, f2, f3, f4))
    print("{} + {}/24 * (9*{} + 19*{} - 5*{} + {})".format(w1[0], h, w_p, f1, f2, f3))
    print("DFSDFS", w1[0] + h/24 * (9*w_p + 19*f1 - 5*f2 + f3))
    return w1[0] + h/24 * (9*w_p + 19*f1 - 5*f2 + f3)

def adaptive_rk4(f, temp, h, t, w, e):
    """
    Uses Runge-Kutta-Fehlberg method of order 5 and Runge Kutta method of
    order four to control the error e. Returns the array consisting of
    the calculated value and q, the scaling factor of h, to see if the value 
    is valid and if not by how much it has to be scaled.
    Round is used to control the floating point errors. 
    """
    
    
    k1 = round((h*f(t, w)), 10)
    k2 = round((h*f(t + 1/4*h, w + 1/4*k1)), 10)
    k3 = round((h*f(t + 3/8*h, w + 3/32*k1 + 9/32*k2)), 10)
    k4 = round((h*f(t + 12/13*h, w + 1932/2197*k1 - 7200/2197*k2 + 7296/2197*k3)), 10)
    k5 = round((h*f(t + h, w + 439/216*k1 - 8*k2 + 3680/513*k3 - 845/4104*k4)), 10)
    k6 = round((h*f(t + h/2, - 8/27*k1 + 2*k2 - 3544/2565*k3 + 1859/4104*k4 - 11/40*k5)), 10)
    w_e4 = round((w + 25/216*k1 + 1408/2565*k3 + 2197/4104* k4 - k5/5), 10)
    w_e5 = round((w + 16/135*k1 + 6656/12825*k3 +28561/56430*k4 - 9/50*k5 + 2/55*k6), 10)
    
    q = 0.84*(e*h/abs(w_e5 - w_e4))**(0.25)
    
    return [w_e4, q]
    

def adaptive_pc(f, temp, h, t, w1, w2, w3, w4, e):
    
    raise Exception("Not Implemented")

