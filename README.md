# Intro

Reads in datafiles from a PPMS 6000 by Quantum Design and fits the specific heat at low temperatures with:


$$C_{V}(T) = \gamma T + \beta T^3$$


And in the full temperature range as $C_p/T^3$ with a Debye and 2 Einstein modes + electronic part:

$$C_{V}(T) = \gamma T + 9 R N_D \left(\frac{T}{\theta_D}\right)^3 \int_{0}^{x_D} \frac{x^4 e^x}{(e^x-1)^2} \ dx +3R \sum_{i} N_{E_i} \frac{\left( \frac{\hbar \omega_{E_i}}{k_B T} \right)^2 e^{\frac{\hbar \omega_{E_i}}{k_B T}}}{\left( e^{\frac{\hbar \omega_{E_i}}{k_B T}}-1\right)^2}$$

This software was written as part of my bachelor thesis at the Vienna University of Technology. It might be useful to others as well.

# Requirments

Needs a python distribution with scipy and numpy.

# License 

               DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                       Version 2, December 2004
    
    Copyright (C) 2016 Benjamin Huber
    
    Everyone is permitted to copy and distribute verbatim or modified
    copies of this license document, and changing it is allowed as long
    as the name is changed.
   
               DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
      TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
   
     0. You just DO WHAT THE FUCK YOU WANT TO.
