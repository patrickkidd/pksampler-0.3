#include "button.inc"

   
#declare Nudge_X = .23;
#declare NudgeArrow = union {
   cylinder {
      <-Nudge_X,0,-Nudge_X>,
      <0,0,0>,
      .05
   }
   cylinder {
      <Nudge_X,0,-Nudge_X>,
      <0,0,0>,
      .05
   }
   cylinder {
      <Nudge_X, 0, .1>,
      <-Nudge_X,0,.1>,
      .05       
   }
   sphere {
      <0,0,0>,
      .05
   }
   sphere {
      <-Nudge_X,0,-Nudge_X>,
      .05
   }
   sphere {
      <Nudge_X,0,-Nudge_X>,
      .05
   }
   sphere {
      <Nudge_X, 0, .1>,
      .05
   }
   sphere {
      <-Nudge_X,0,.1>,
      .05
   }
   pigment { White }
   finish { ambient .4 }
   scale <1,1.1,1>
}   

#declare NudgeUpLabel = union {
   NudgeArrow
   translate <0,.2,.075>
}   

#declare NudgeDownLabel = union {
   NudgeUpLabel
   rotate y*180
}


#macro DrawNudgeUpButton(Color)

difference {
   DrawButton(Color)
   TranslateForButton(NudgeUpLabel)
}                     
   
#end

#macro DrawNudgeDownButton(Color)

difference {
   DrawButton(Color)
   TranslateForButton(NudgeDownLabel)
}                     
   
#end
