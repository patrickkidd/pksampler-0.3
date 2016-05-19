#include "button.inc"     
     
              
                            
#declare GroupLabel = text {
   ttf "ARIALBI.TTF" "Group" .2, 0
   pigment { color White }
   finish { ambient .6 }
   rotate x*90
   translate <0,.5,0>
   scale <.4,.5,.45>
} 
                           
     
     
#macro DrawGroupButton(Color)

difference {
   DrawButton(Color)
   object {
      TranslateForButton(GroupLabel)
      translate <-.6,0,-.1>
      //scale <1.1,1,1>
   }
}

#end
