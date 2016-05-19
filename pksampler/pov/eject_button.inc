#include "button.inc"     
     

#declare Eject_X = .25;
#declare Eject_Z = -.4;
#declare Eject_Space = .12;

#declare EjectLabel = union {
        
   // bottom line
   cylinder {
      <-Eject_X, 0, -Eject_Space>,
      <Eject_X ,0, -Eject_Space>,
      .05
   }   
   sphere {
      <-Eject_X , 0, -Eject_Space>,
      .05
   }
   sphere {
      <Eject_X, 0, -Eject_Space>,
      .05
   }  
          
   union { 
      // bottom triangle line
      cylinder {
         <-Eject_X, 0, 0>,
         <Eject_X ,0, 0>,
         .05
      }   
      sphere {
         <-Eject_X , 0, 0>,
         .05
      }
      sphere {
         <Eject_X, 0, 0>,
         .05
      }
      
      // slanted lines
      cylinder {
         <-Eject_X, 0, 0>
         <0,0,-Eject_Z>,
         .05
         pigment { color <.8,.8,.8> }
         finish { ambient .4 }
      }
      cylinder {
         <Eject_X, 0, 0>
         <0,0,-Eject_Z>,
         .05
      }
      sphere {
         <0, 0, -Eject_Z>,
         .05
      }
   
      pigment {
         gradient x 
         color_map {
            [-Eject_X color <.8,.8,.8>]
            [Eject_X color White]
         }
         translate <-Eject_X-.05,0,0>
      }   
      finish { ambient .4 } 
   }     
   pigment { White }
   finish { ambient .4 }
   translate <0,.19,-.11>
   scale <1.2,1,1>   
}
                           
     
     
#macro DrawEjectButton(Color)

difference {
   DrawButton(Color)
   TranslateForButton(EjectLabel)
}

#end
