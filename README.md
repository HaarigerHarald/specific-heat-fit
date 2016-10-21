# Intro

Reads in datafiles from a PPMS 6000 by Quantum Design and fits the specific heat at low temperatures with:


<img src="http://www.sciweavers.org/tex2img.php?eq=C_%7BV%7D%28T%29%20%3D%20%5Cgamma%20T%20%2B%20%5Cbeta%20T%5E3&bc=Transparent&fc=Black&im=png&fs=18&ff=concmath&edit=0" align="center" border="0" alt="C_{V}(T) = \gamma T + \beta T^3" width="212" height="31" />


And in the full temperature range as Cp/T^3 with a Debye and 2 Einstein modes + electronic part:

<img src="http://www.sciweavers.org/tex2img.php?eq=C_%7BV%7D%28T%29%20%3D%20%5Cgamma%20T%20%2B%209%20R%20N_D%20%5Cleft%28%5Cfrac%7BT%7D%7B%5Ctheta_D%7D%5Cright%29%5E3%20%5Cint_%7B0%7D%5E%7Bx_D%7D%20%5Cfrac%7Bx%5E4%20e%5Ex%7D%7B%28e%5Ex-1%29%5E2%7D%20%5C%20dx%20%2B3R%20%5Csum_%7Bi%7D%20N_%7BE_i%7D%20%5Cfrac%7B%5Cleft%28%20%5Cfrac%7B%5Chbar%20%5Comega_%7BE_i%7D%7D%7Bk_B%20T%7D%20%5Cright%29%5E2%20e%5E%7B%5Cfrac%7B%5Chbar%20%5Comega_%7BE_i%7D%7D%7Bk_B%20T%7D%7D%7D%7B%5Cleft%28%20e%5E%7B%5Cfrac%7B%5Chbar%20%5Comega_%7BE_i%7D%7D%7Bk_B%20T%7D%7D-1%5Cright%29%5E2%7D&bc=Transparent&fc=Black&im=png&fs=18&ff=concmath&edit=0" align="center" border="0" alt="C_{V}(T) = \gamma T + 9 R N_D \left(\frac{T}{\theta_D}\right)^3 \int_{0}^{x_D} \frac{x^4 e^x}{(e^x-1)^2} \ dx +3R \sum_{i} N_{E_i} \frac{\left( \frac{\hbar \omega_{E_i}}{k_B T} \right)^2 e^{\frac{\hbar \omega_{E_i}}{k_B T}}}{\left( e^{\frac{\hbar \omega_{E_i}}{k_B T}}-1\right)^2}" width="785" height="123" />


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