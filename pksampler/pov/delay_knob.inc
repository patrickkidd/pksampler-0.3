#include "knob.inc"             
  
  
#declare EchoWave = union {
             
   difference {  
      torus {
         .3,
         .07           
      }
      
      box {
         <0,-.1,.4>,
         <1,.4,-.4>
         rotate y*10         
      }   
      box {
         <0,-.1,.4>,
         <1,.4,-.4>
         rotate y*-10       
      }
   }
   
   sphere {
      <0,0,.3>, 
      .07  
      rotate y*-10       
   } 
   sphere {
      <0,0,-.3>,
      .07  
      rotate y*10        
   }
   cylinder {
      <-.1,0,0>,
      <.01,0,0>,
      .07
   } 
   sphere {
      <-.1,0,0>,
      .07       
   }   
   sphere {
      <.01,0,0>,
      .07       
   }            
   scale <1.1,1,.6> 
   rotate y*180
}

#declare DelayKnobLabel = union {
   object {
      EchoWave
      pigment { White }
      finish { ambient .4 } 
      translate <-.65,0,.9>
   }
   object {
      EchoWave
      pigment { color <.8,.8,.8> }
      finish { ambient .4 }  
      translate <-.15,0,.9>
   }
   object {
      EchoWave
      pigment { color <.6,.6,.6> }
      finish { ambient .4 }  
      translate <.35,0,.9>
   }
}


#macro DrawDelayKnob()
   DrawKnob()
   KnobLEDBulb
   DelayKnobLabel
#end
