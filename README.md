[Project description](https://math.gsu.edu/xye/course/na_handout/project/proj1.pdf)  
  
### To run:
`python main.py [all|methods_to_run]`  
  
Ex:  
`python main.py all` - to run all methods on all examples  
`python main.py euler` - to run euler's method on all examples  
`python main.py euler 1` - to run euler's method on example 1  
`python main.py rk4 euler` - to rk4 and euler's methods on all examples  
`python main.py rk4 euler 2` - to rk4 and euler's methods on example 2  
`python main.py rk4 plot euler 2` - to plot rk4 and euler's methods errors on example 2  
`python main.py rk4 plot values euler 2` - to plot rk4 and euler's method values errors on example 2  
`python main.py rk4 plot solution euler 2` - to plot rk4 and euler's method values on example 2, along with its exact solution

### TODOS:
- [x] euler's method
- [x] iteration abstraction system for 1 dimension
- [x] modified euler's method (Ratislav)
- [x] rk2 (Ratislav)
- [ ] rk4 (Ratislav)
- [ ] ab_four_step_explicit (Caleb)
- [ ] predictor_corrector (Ratislav)
- [ ] adaptive step size: rk4 (Ratislav)
- [ ] adaptive step size: predictor-corrector (Ratislav)
- [x] iteration abstraction system for 2+ dimensions (Caleb)


### For Report:
Do on Friday
- [ ] Intro
- [ ] Summary
- [ ] Discussion

Methods:
- [ ] Euler (caleb)
- [ ] Modified Euler (Ratislav)
- [ ] Rk2 (Ratislav)
- [ ] RK4 (caleb)
- [ ] AB four step explicit (caleb)
- [ ] Predictor Corrector (caleb)
- [ ] Adaptive RK4 (Ratislav)
- [ ] Adaptive Predictor Corrector (Ratislav)
Expirements
- [ ] Example 1 (Ratislav)
- [ ] Example 2 (caleb)
- [ ] Example 3 (Ratislav)
- [ ] Example 4 (caleb)

Expirment structure:
1. Show the equation (with step size, and bounds, etc.)
2. Show equation for and plot the solution
3. Plot errors for each method on same graph 
4. Plot top 3 performers on the solution along with the solution on same graph

## Highlights from description:
### Methods:
- Euler’s method and modified Euler’s method
- Midpoint (RK2) and Runge-Kutta 4th-order (RK4) methods 
- Adams-Bashforth (AB) four-step explicit method 
- Predictor-corrector method using AB 4-step explicit and Adams-Moulton 3-step implicit scheme. 
- Adaptive step size RK4 method (extra credit) 
- Adaptive step size Predictor-Corrector method (extra credit)

### Miscellaneous
- 1 dimensional case is required, 2+ Dimensions is extra credit
---

## Authors
- Ratislav Krylov
- Caleb Lewis

**Due date: March 2, 2018**
