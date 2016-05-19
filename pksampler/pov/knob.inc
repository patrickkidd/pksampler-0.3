#include "pksampler.inc"
#include "metals.inc"
#include "textures.inc"


#declare KnobCone = cone {
   <0,.1,0>,
   .55,
   <0,.4,0>,
   .37
   pigment { color <.7,.7,.7> }
   finish { phong 1 ambient .4 reflection .4}
}

#declare KnobNotchColor = color <1,1.05,1.05>;

#declare KnobNotch = cylinder {
   <0,0,0>,
   <0,.5,0>,
   .17                 
   pigment { KnobNotchColor }
   rotate z*-12
   translate <-.55,.16,0>
   finish { phong 1  reflection .1}
}


#macro Knob()

   difference {
      object {
         KnobCone
         finish { phong 1 }
      }
   
   #local deg = 0;
   #while(deg < 360)
      #local deg = deg + (360 / 8);
      object {
         KnobNotch
         rotate y*deg
      }
   #end
   
      sphere {
         <0,.7,0>,
         .5 
         pigment { KnobNotchColor }
         finish { phong 1 }
         scale <1,1.4,1>
      }
   }
   
#end



#macro DrawKnob()
   object {
      Knob()  
      rotate y*((clock/127)*270)
      translate <.3,0,0>
      finish { phong 1 ambient .2 reflection 1}
   }
#end 



#declare KnobLEDBox = box {
   <-.3,-.3,-.11>,
   <.1,.001,0>
   pigment { White }
   finish { ambient .3 }
}

#macro KnobLEDPigment()
   pigment {
      gradient z
      color_map {
         [.4 color <1.7,0,0>]
         [.6 color <0,1.7,0>]
         [.76 color <1.7,1.7,0>]
      }
      scale 2
      translate -1
   }
#end

#declare KnobLEDBulb = light_source {
   0
   color Red
   spotlight
   point_at <-.3,100,-.55>
   //falloff 45
   //radius 30 
   looks_like {
      box {
         <-.3,0,.5>,
         <.3,1,-.6>
         KnobLEDPigment() 
         translate <-.6,-1.04,-1.01+((clock/127)*.97)>
      }
   }
}

#declare KnobIndentShape = union {
   object {
      KnobLEDBox
      translate <-.5,0,-.38>
   }
   object {
      KnobLEDBox
      translate <-.5,0,-.19>
   }
   object {
      KnobLEDBox
      translate <-.5,0,-.01>
   }
   object {
      KnobLEDBox
      translate <-.5,0,.17>
   }
   object {
      KnobLEDBox
      translate <-.5,0,.35>
   }
   object {
      KnobLEDBox
      translate <-.5,0,.53>
   }
      
   #if(clock > 3)
      union {
         // bottom
         cylinder {
            <-.83,0,-.54>,
            <-.37,0,-.54>,
            .015
         }
         // left
         cylinder {
            <-.83,0,.53>,
            <-.83,0,-.53>,
            .015
         }
         // top
         cylinder {
            <-.83,0,.53>,
            <-.38,0,.53>,
            .015
         }
         // right
         cylinder {
            <-.37,0,-.54>,
            <-.37,0,.53>,
            .015
         }
         pigment { color <.5,.5,.5> }
         finish { ambient .2 }
         scale <1,3,1>
         translate <0,-.025,0>
      }
   #end
   translate <0,0,-.04>                      
}      

