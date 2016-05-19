#include "button.inc"     
     

#declare Unload_W = .27;

#declare UnloadLabel = union {
   
   torus {
      Unload_W,
      .05
   }
   
   union {
      cylinder {
         <0,0,Unload_W>,
         <0,0,-Unload_W>,
         .05
         rotate y*45 
      }
      cylinder {
         <0,0,Unload_W>,
         <0,0,-Unload_W>,
         .05
         rotate y*-45
      }
      pigment { color <.8,.8,.8> }
      finish { ambient .4 }
   }
   
   union { 
      // dots
      sphere {
         <-.17,0,0>,
         .04
      }
      sphere {
         <.17,0,0>,
         .04
      }
      // rounded edges
      sphere {
         <0,0,.17>,
         .04
      }
      sphere {
         <.0,0,-.17>,
         .04
      }
      pigment { color <.7,.7,.7> }
      finish { ambient .4 }
   }       
         
   
   finish { ambient .4 }
   pigment { White }
   translate <0,0,-.07>   
} 
                           
     
     
#macro DrawUnloadButton(Color)

difference {
   DrawButton(Color)
   object {
      TranslateForButton(UnloadLabel)
      translate <0,.19,.1>
      scale <1.1,1,1>
   }
}

#end
