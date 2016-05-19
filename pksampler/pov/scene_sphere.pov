#include "colors.inc"              
              
              
light_source { 
   <-600, 900, 600>
   color White
   area_light <700, 0, 0>, <0, 0, 700>, 8, 8
   fade_distance 100
}
   
camera {
   location <0, 20, 0> // original
   //location <6.5,1.9,-3.4>
   look_at 0
   //look_at <-2.5,-1.4,0>
   angle 36
}

plane {
   y, 0
   pigment { White }
   finish { ambient .5 }
}                   


sphere {
   <0,0,0>,
   3
   pigment {
      image_map {
         png
         "pksampler_scr.png"
         map_type 0
      }          
      translate <-.5,0,0>
      rotate x*90 
      scale 5
   }
   finish { ambient .9 }
} 

sphere {
   <0,0,0>,
   .5
   pigment {
      image_map {
         png
         "scene.png"
         map_type 0
      }          
      translate <-.5,0,0>
      rotate x*90 
      scale 1
   }
   finish { ambient 1 }
   translate <5,0,0>
   rotate y*-25
}

sphere {
   <0,0,0>,
   1
   pigment {
      image_map {
         gif
         "arranger-big.gif"
         map_type 0
      }          
      translate <-.5,0,0>
      rotate x*90
      rotate y*-25 
      scale 5
   }
   finish { ambient 1 }
   translate <4.5,0,0>
   rotate y*25
}