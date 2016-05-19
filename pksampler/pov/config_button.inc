#include "button.inc"


#declare ConfigLabel = union {

   torus {
      .4, .07
   }
#local i=0;
#while(i<=10)
   cylinder {
      <.4,0,.4>,
      <.3,0,.3>, 
      .07
      rotate y*((36*i) + 180) /* inc the color, flip the gradient */
      #declare Delta = .3 * (i/10);
      pigment { color <.7+Delta,.7+Delta,.7+Delta> }
      finish { ambient .4 }
   }
#local i = i + 1;     
#end 
   sphere {
      0,.07
   }
   pigment { White } 
   finish { ambient .4 }
   translate <0,.19,0>
   scale <.65,1,.65>
   
}

#macro DrawConfigButton(Color)
   difference {
      DrawButton(Color)
      TranslateForButton(ConfigLabel)
   }
#end


