#include "button.inc"

#declare CueZoneWidth = .22;

#declare CueZonePhoneCup = difference {
   sphere {
      0,CueZoneWidth
   }  
   box {
      <0,1,1>,
      <1,-1,-1>
   }
}

#declare CueZoneLabel = union {
   difference {
      torus {
         CueZoneWidth,.05
         translate <0,0,CueZoneWidth>
      }
      box {
         <-1,-1,-1>,
         <1,1,CueZoneWidth>
      }
   }
   object {
      CueZonePhoneCup
      translate <-.2,0,0>
   }
   object {
      CueZonePhoneCup   
      rotate y*180
      translate <.2,0,0>
   }
   finish { ambient .4 }
   pigment { White }
   scale <1,.4,.8>
   translate <-.01,0,-.09>
}       

#macro DrawCueZoneButton(Color)
      
difference {
   DrawButton(Color)
   object {
      TranslateForButton(CueZoneLabel)
      translate <0,.18,0>
   }
}

#end


