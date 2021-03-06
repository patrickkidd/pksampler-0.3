#include "pksampler.inc"

// horizontal search slider


PK_Camera()
PK_Light()

#declare GrooveHeight = 3.1;


difference {
   
   PK_Plane()
   
   box {
      <-3.1, .1, .3>,
      <3.1,-.07,-.3>
      pigment { White }
      finish {
         phong .4
         ambient .1
      }
   }   
   
   box {
      <-2.9, -.3, .02>,
      <2.9, 0.7, -.02>
      pigment { Black }
   }
}
   
        
#declare SearchCoef = .87;        
cylinder {
   <0,0,.3>,
   <0,0,-.3>,
   .3
   pigment { PKGreen }
   scale <1.3,.6,1>
   finish { phong 1 ambient .05 }                                  
   //finish { ambient .2 } 
   translate <-GrooveHeight * SearchCoef + ((GrooveHeight/127) * clock) * 2 * SearchCoef, 0, 0>
}


