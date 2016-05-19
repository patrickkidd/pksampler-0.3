#include "pksampler.inc"


PK_Camera()
PK_Light()

PK_Plane()


#declare ToggleShape = cylinder {
   <0,-1.5,0>,
   <0,.5,0>,
   .1
   pigment { Green }
   rotate x*45
}


                                 
#declare ToggleIndentShape = superellipsoid {
   <1,0>

}

object {
   ToggleIndentShape
   pigment { Green }
}