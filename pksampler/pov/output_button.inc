#include "button.inc"
#declare Nudge_X = .2;                                       
                                                            
#declare OutputLabel = union {
   
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


#macro DrawOutputButton(Color)

difference {
   DrawButton(Color)
   OutputLabel
}

#end
