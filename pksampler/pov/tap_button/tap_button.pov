
#include "tap_button.inc"


PK_Light()
//PK_Camera()
/*
camera {
   //location <0, 20, 0> // original
   location <6.5,1.9,-3.4>
   //look_at 0
   look_at <-2.5,-1.4,0>
   angle 36
}
*/

   camera {
      //location <0, 15, 0> // original
      //location <0,3,0>
      location <1.6,.3,-2>
      look_at <-0,0,-0>
      angle 36
   }

difference {
   PK_Plane()
   TapButtonIndentShape
}

DrawTapButton(Green)
 