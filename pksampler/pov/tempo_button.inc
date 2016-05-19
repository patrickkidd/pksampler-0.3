#include "button.inc"     
     

#declare Tempo_X = .3;

#declare TempoLabel = union {
          
   torus {
      Tempo_X,.070
   }
   
   // the clock hands
   union {          
      // longer line
      union {
         cylinder {
            <0, 0, 0>,
            <Tempo_X*.6, 0, 0>,
            .05
         }   
         sphere {
            <0,0,0>,
            .05
         }
         sphere {
            <Tempo_X*.6, 0, 0>,
            .05
         }
         rotate y*-15
      }
      
      // shorter line
      union {
         cylinder {
            <0, 0, 0>,
            <Tempo_X*.45, 0, 0>,
            .05
         }   
         sphere {
            <0,0,0>,
            .05
         }
         sphere {
            <Tempo_X*.45, 0, 0>,
            .05
         }
         rotate y*70
      }
      pigment { color <.9, .7, .6> }
      finish { ambient .5 }
   }  
   
     
   pigment { White }
   finish { ambient .4 }
   translate <0,.19,0>
}
                           
     
     
#macro DrawTempoButton(Color)

difference {
   DrawButton(Color)
   TranslateForButton(TempoLabel)
}

#end

