#include "pksampler.inc"
#include "button.inc"

// A still image that says "drag me" for Sample.Sample

PK_Camera()
PK_Light()


#declare DragmeLabel1 = text {
   ttf "ARIALBI.TTF" "drag" .2, 0
   pigment { color White }
   finish { ambient .4 }
   rotate x*90
   translate <-1,0,.1>
   scale <.7,1,.4> 
}
#declare DragmeLabel2 = text {
   ttf "ARIALBI.TTF" "me" .2, 0
   pigment { color White }
   finish { ambient .4 }
   rotate x*90
   translate <-.7,0,-1>
   scale <.7,1,.4> 
}



//difference {
   PK_Plane()
   /*
   superellipsoid {
      <.5,.5>
      pigment { White }
      finish { ambient .2 } 
      //translate <0,.1,0>
      scale <1.25,.05,.5>
   }
}    
*/

#declare DragmeLabel = union {
   object { DragmeLabel1 }
   object { DragmeLabel2 }
}

object {
   DragmeLabel
   translate <0,.1,.05>
   scale <1,1,.9>
}




          
          