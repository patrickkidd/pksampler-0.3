#include "button.inc"


#declare SaveLabel = union {
   
   // left 
   cylinder {
      <-.4,0,-.4>,
      <-.4,0,.4>,
      .1
   }
   // right
   cylinder {
      <.4,0,-.3>,
      <.4,0,.4>,
      .1
   }
   

   // top
   cylinder {
      <.4,0,.4>,
      <-.4,0,.4>,
      .1
   }
   // bottom
   cylinder {
      <-.4,0,-.4>,
      <.3,0,-.4>,
      .1
   }
   // roundies
   sphere {
     <-.4,0,-.4>,
     .1
   }

   sphere {
     <-.4,0,.4>,
     .1
   }
   sphere {
      <.4,0,.4>,
      .1
   }   
   
   
   // grey group
   
   union {
   
      // notch
      cylinder {
         <.3,0,-.4>,
         <.4,0,-.3>,
         .1
      }
      sphere {
        <.4,0,-.3>,
        .1
      }
      sphere {
        <.3,0,-.4>,
        .1
      }
      
      // door
      cylinder {
         <.15,0,-.4>,
         <.15,0,0>,
         .1
      }
      cylinder {
         <-.15,0,-.4>,
         <-.15,0,0>,
         .1
      }
      cylinder {
         <-.15,0,0>,
         <.15,0,0>,
         .1
      }
      sphere {
         <-.15,0,0>,
         .1
      }
      sphere {
         <.15,0,0>,
         .1
      }
      pigment { color <.8,.8,.8> }
      finish { ambient .4 } 
   }

    
   pigment { White } 
   finish { ambient .4 }
   translate <0,.19,.05>
   scale <.65,1,.65>
   
}

#macro DrawSaveButton(Color)
   difference {
      DrawButton(Color)
      TranslateForButton(SaveLabel)
   }   
#end

