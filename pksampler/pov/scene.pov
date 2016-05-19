\#include "scene.inc"

PK_Light()
camera {
   //location <0, 20, 0> // original
   location <6.5,1.9,-3.4>
   //look_at 0
   look_at <-2.5,-1.4,0>
   angle 36
}

TrackFacePlate
TrackControls
                         
union {                         
   object { TrackFacePlate }
   object { TrackControls }
   translate <-7.6, 0, 0>

}   

union {                         
   object { TrackFacePlate }
   object { TrackControls }
   translate <-15.2, 0, 0>
}
 
                       

 
   
   


   
