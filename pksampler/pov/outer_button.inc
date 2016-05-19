#include "button.inc"

#declare OutputLabel = union {
   
   cylinder {
      <-.5, 0, .5>,
      <1.1, 0, .5>,
      .05
   }
   sphere {
      <-.5, 0, .5>,
      .05
   }
   sphere {
      <1.1, 0, .5>,
      .05
   }   
}

#macro DrawOutputButton(Color)
   difference {
      DrawButton(Color)
      TranslateForButton(OutputLabel)
   }
#end
