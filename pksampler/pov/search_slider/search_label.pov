#include "pksampler.inc"


PK_Camera()
PK_Light()

difference {
   PK_Plane()
   sphere {
      0,.7
      translate <0,.3,0>
      pigment { White }
      finish {
         phong 1
         reflection .6 
      }
   }
}

union {
   torus {
      .7,
      .1
      pigment { White }
   }

   cylinder {
      0,
      <.7,0,0>,
      .1
   }
   sphere {
      0,
      .1
   }

   pigment { White }
   finish {
      phong 1
   }
}