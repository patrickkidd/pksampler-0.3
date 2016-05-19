#include "button.inc"

#declare MainZoneWidth = .2;

#declare MainZoneLabel = union {
   
   // speaker
   cylinder {
      <-.02,0,0>,
      <.1,0,0>,
      MainZoneWidth
   }
   cone {
      <.09,0,0>,
      MainZoneWidth,
      <.3,0,0>,
      MainZoneWidth*2.2
   }
   
   //sound waves
   cylinder {
      <.4,0,.2>,
      <.65,0,.3>
      .05
   }
   cylinder {
      <.4,0,-.2>,
      <.65,0,-.3>
      .05
   }
   cylinder {
      <.4,0,0>,
      <.55,0,0>
      .05
   }
   scale <1,.4,.7>
   pigment { White }
   finish { ambient .4 }
}       

#macro DrawMainZoneButton(Color)
      
difference {
   DrawButton(Color)
   object {
      TranslateForButton(MainZoneLabel)
      translate <-.2,.18,0>
   }
}

#end
    
