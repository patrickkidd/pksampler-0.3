#include "button.inc"     
     

#declare Pause_Z = .22;

#declare PauseLabel = union {
   
   cylinder {
      <-.15,0,Pause_Z>,
      <-.15,0,-Pause_Z>,
      .05
   }
   cylinder {
      <.15,0,Pause_Z>,
      <.15,0,-Pause_Z>,
      .05
   }
   // rounded edges
   sphere {
      <-.15,0,Pause_Z>,
      .05
   }
   sphere {
      <-.15,0,-Pause_Z>,
      .05
   }
   // rounded edges
   sphere {
      <.15,0,Pause_Z>,
      .05
   }
   sphere {
      <.15,0,-Pause_Z>,
      .05
   }       
         
   pigment { White }
   finish { ambient .4 }
   translate <0,0,-.07>   
} 
                           
     
     
#macro DrawPauseButton(Color)

difference {
   DrawButton(Color)
   object {
      TranslateForButton(PauseLabel)
      translate <0,.19,.1>
      scale <1.1,1,1>
   }
}

#end
