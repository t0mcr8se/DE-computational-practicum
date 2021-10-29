# Differential Equations: Computational Practicum

## Report:
Name: Mohammad Rami Husami
Group: B20-04

## Exact Solution:
![img1](assets/eq1.png)

![img2](assets/eq2.png)

This is the Bernoulli equation, let's solve it.

First we should divide both parts by `y^(2/3)`

We get

![im3](assets/eq3.png)

then5 make the following substitution

![im4](assets/eq4.png)

We get

![im5](assets/eq5.png)

Equation (1) is a first-order non-homogeneous linear ordinary differential equation.

First we need to solve the complementary equation

![im6](assets/eq6.png)

Substitute to Equation (1)

![im7](assets/eq7.png)

Back substitution

![im8](assets/eq8.png)

So, let's find `C3`

![im9](assets/eq9.png)

### Answer:

![im10](assets/eq10.png)



## Results

### Solutions charts
![solutions](assets/gui1.png)

Chart of solution and approximate values.

We can notice that the Runge-Kutta methods calculates the most approximate values, the worst approximation is done by the Euler method.


### LTE charts
![LTE](assets/gui2.png)

Also we can see that the Runge-Kutta methods has the smallest error and the Euler has larger errors.


### Global Errors chart
![GTE](assets/gui3.png)

We can see here that if we increase the steps, the value of GTE decreases.

### UML Diagram
![UML](assets/uml.png)