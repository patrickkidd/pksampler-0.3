#include "button.inc"

   
#declare PitchCenterLabel = union {

   text {
      ttf "ARIALBI.TTF" "0.0" .2, 0
      pigment { color White }
      finish { ambient .6 }
      rotate x*90
      translate <-1,.5,-.3>
      scale <.5,.5,.55>      
   }  
   text {
      ttf "ARIALBI.TTF" "%" .2, 0
      pigment { color White }
      finish { ambient .6 }
      rotate x*90
      translate <.8,.5,-.375>
      scale <.3,.5,.4>      
   }
   translate <.03,0,0>
   scale <.9,1,.9>   
}   


#macro DrawPitchCenterButton(Color)

difference {
   object {
      DrawButton(Color)
      scale <.75,1,1>
   }
   TranslateForButton(PitchCenterLabel)
}                     
   
#end
