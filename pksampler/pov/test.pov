
#include "colors.inc"

   camera {
      location <0, 15, 0> // original
      //location <-1,3,-2>
      //location <-7,1,0>
      look_at 0
      angle 36
   }


   light_source { 
      <-600, 900, 600>
      color White
      area_light <700, 0, 0>, <0, 0, 700>, 8, 8
      fade_distance 100
   }

   plane {
      y, 0
      pigment { White }
   }

sphere {
   <0,.3,0>,
   .5 
   pigment { Red }
   finish { phong 1 }
   scale <1,1.5,1>
}
