#include "button.inc"

#declare ExitLabel = union {    
    torus {
       .4,.07
    }  
    cylinder {
       <0,0,.25>,
       <0,0,-.25>,
       .07
    }
    sphere {
       <0,0,.25>,
       .07
    }
    sphere {
       <0,0,-.25>,
       .07
    }
    pigment { White }
    finish { ambient .4 }
    translate <0,.19,0>        
 }    
 
#macro DrawExitButton(Color)
difference {
   object {
      DrawButton(Color)
      scale <1,1,1.5>
   }
   TranslateForButton(ExitLabel)
}                           

#end
