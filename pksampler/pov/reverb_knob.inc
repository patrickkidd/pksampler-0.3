#include "knob.inc"             
  
  
#declare ReverbWave = union {
             
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
   //finish { ambient .4 } 
}
     

#declare ReverbSphere = sphere {
   <0,0,.9>,
   .07
}

#declare ReverbKnobLabel = union {

   union {
      object {
         ReverbSphere
         translate <0,0,0>
      }
      object {
         ReverbSphere
         translate <.2,0,.1>
      }
      object {
         ReverbSphere
         translate <.2,0,-.1>
      }
      object {
         ReverbSphere
         translate <.4,0,-0>
      }
      object {
         ReverbSphere
         translate <.5,0,.2>
      }
      object {
         ReverbSphere
         translate <.5,0,0-.15>
      }
      object {
         ReverbSphere
         translate <.6,0,0>
      }
      object {
         ReverbSphere
         translate <.8,0,-.1>
      }
      object {
         ReverbSphere
         translate <.8,0,0.2>
      }
      pigment {
         gradient x
         color_map {
            [.1 color White]
            [.7 color Black]
         }
         scale 2
         translate <-.1,0,0>
      }
      finish { ambient .4 }
      translate <-.1,0,0>
   }
   
      
   object {
      ReverbWave
      pigment { White }
      finish { ambient .4 }
      translate <-.35,0,.9>
   }
}

#macro DrawReverbKnob()
   
   DrawKnob()
   KnobLEDBulb
   ReverbKnobLabel

#end
