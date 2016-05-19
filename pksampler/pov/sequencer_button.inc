#include "button.inc"     
                               
     
#declare SequencerLabel = union {
   text {
      ttf "arialbi.ttf" "Seq." .2, 0
      pigment { color White }
      finish { ambient .6 }
      rotate x*90
      translate <.45,.55,.05>
      scale <.4,.4,.45>
   }
 
	/*                            
   text {
      ttf "arialbi.ttf" "edit" .2, 0
      pigment { color White }
      finish { ambient .6 }
      rotate x*90
      translate <.5,.5,-.5>
      scale <.2,.2,.45>
   } 
*/
                                    
   translate <-.6,0,-.1>
};


     
#macro DrawSequencerButton(Color)

difference {
   DrawButton(Color)
   TranslateForButton(SequencerLabel)
}

#end
