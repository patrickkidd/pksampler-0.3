#include "button.inc"     
                               
     
#declare AutoGroupLabel = union {
   text {
      ttf "ARIALBI.TTF" "Group" .2, 0
      pigment { color White }
      finish { ambient .6 }
      rotate x*90
      translate <0,.5,.35>
      scale <.4,.4,.45>
   }
                            
   text {
      ttf "ARIALBI.TTF" "edit" .2, 0
      pigment { color White }
      finish { ambient .6 }
      rotate x*90
      translate <.5,.5,-.5>
      scale <.4,.4,.45>
   } 
                                    
   translate <-.6,0,-.1>
};


     
#macro DrawGroupEditButton(Color)

difference {
   DrawButton(Color)
  TranslateForButton(AutoGroupLabel)
}

#end
