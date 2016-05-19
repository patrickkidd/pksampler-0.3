#include "pksampler.inc"
                      
PK_Camera()
PK_Light()
PK_OuterPlane()

#macro DrawLabel(string,X)
   text {
      ttf "ARIALBI.TTF" string .2, 0
      pigment { Green }
      finish { ambient .5 }
      rotate x*90
      translate <-1.25+X,.1,-.7>
      scale <.5,2,.5>
   } 
#end
   
 
 
DrawLabel("RealTime", 0)     