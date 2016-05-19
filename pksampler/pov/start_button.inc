#include "tap_button.inc"


#declare StartButtonZVal = .26;
#declare StartLabel = union {
   cylinder {
      <0,0,0>,
      <-StartButtonZVal,0,StartButtonZVal>,
      .05
   }
   cylinder {
      <0,0,0>,
      <-StartButtonZVal,0,-StartButtonZVal>,
      .05
   }
   
   // roundies
   sphere {
      <0,0,0>,
      .05
   }
   sphere {
      <-StartButtonZVal,0,StartButtonZVal>,
      .05
   }
   sphere {
      <-StartButtonZVal,0,-StartButtonZVal>,
      .05
   }
   
   pigment { White }
   finish { ambient .4 }
   scale <1,1.1,1>
   translate <0.2,.08,.03>
}

  
#macro DrawStartButton(Color)
   difference {
      DrawTapButton(Color)
      TranslateForTapButton(StartLabel)       
   }
#end
 
