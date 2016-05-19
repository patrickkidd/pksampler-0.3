#include "button.inc"

#switch(clock)
 #range(0,99)
   #declare x_off = .4;
 #break
 #range(100,999)
   #declare x_off = .2;
 #berak            
 #range(1000,9999)
   #declare x_off = 0;
 #break                              
 #else
#end 
                                   
#declare NumberButtonLabel = text {
   ttf "arialbi.ttf" str(clock,1,0) .2, 0
   pigment { color White }
   finish { ambient .4 }
   rotate x*90
   translate <x_off,.5,-.3>
   scale <.8,.5,.4> 
}

#macro DrawNumberButton(Color)
   difference {
      DrawButton(Color)
      TranslateForButton(NumberButtonLabel)
   }
#end
