#include "button.inc"     
                               
     
#declare AutoGroupLabel = union {
   text {
      ttf "ARIALBI.TTF" "Auto" .2, 0
      pigment { color White }
      finish { ambient .6 }
      rotate x*90
      translate <.3,.5,.35>
      scale <.4,.5,.45>
   }
                            
   text {
      ttf "ARIALBI.TTF" "start" .2, 0
      pigment { color White }
      finish { ambient .6 }
      rotate x*90
      translate <.3,.5,-.4>
      scale <.4,.5,.45>
   } 
                                    
   translate <-.6,0,-.1>
};


     
#macro DrawAutoGroupButton(Color)

difference {
   DrawButton(Color)
  TranslateForButton(AutoGroupLabel)
}

#end
