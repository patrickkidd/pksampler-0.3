#include "button.inc"
 

#declare PitchUpLabel = union {
   
   // curve
   difference {
      torus {
         .3,
         .05
      }
      box {
         .5,-.5
         translate <0,0,-.5>
      }
   }
   
   // rounded edges
   sphere {
      <-.3,0,0>,
      .05
   }
   sphere {
      <.3,0,0>,
      .05
   }
   
   // dot
   sphere {
      <0,0,.1>,
      .05
   }      
         
   pigment { White }
   finish { ambient .4 }   
}

  

#declare PitchDownLabel = union {
   
   // curve
   difference {
      torus {
         .3,
         .05
      }
      box {
         .5,-.5
         translate <0,0,.5>
      }
   }
   
   // rounded edges
   sphere {
      <-.3,0,0>,
      .05
   }
   sphere {
      <.3,0,0>,
      .05
   }
   
   // dot
   sphere {
      <0,0,-.1>,
      .05
   }      
         
   pigment { White }
   finish { ambient .4 }   
} 

#macro DrawPitchUpButton(Color)

difference {
   DrawButton(Color)
   object {
      TranslateForButton(PitchUpLabel)
      translate <0,.19,-.1>
      scale <1.1,1,1>
   }
}

#end
    
#macro DrawPitchDownButton(Color)

difference {
   DrawButton(Color)
   object {
      TranslateForButton(PitchDownLabel)
      translate <0,.19,.1>
      scale <1.1,1,1>
   }
}

#end          
 