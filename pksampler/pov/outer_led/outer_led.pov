#include "pksampler.inc"


PK_Camera()
PK_Light()
PK_OuterPlane()


#declare Width = .3;
#declare Lum = .5;

torus {
   Width,
   (Width * .2)
   pigment { White }
   translate <0,.1,0>
}

light_source {
   0, color Green
   looks_like {
      sphere {
         0,Width
         
         // the color/intensity
         #if(clock <= 0 )
            pigment { color 0 }
         #end
         #if(clock > 0 & clock <=1 )
            pigment { color <0,clock+Lum,0> } //color <.1,.1,clock>  }
         #end
         #if(clock > 1 & clock <= 2 )
           #declare ElseClock = clock - 1;
            pigment { color <ElseClock+Lum,0,0> }
         #end
         #if(clock > 2 & clock <= 3 )
           #declare ElseClock = clock - 2;
            pigment { color <0,0,ElseClock+Lum> }
         #end
         
      }
      finish {
        phong 1
      }
   }
}
      

