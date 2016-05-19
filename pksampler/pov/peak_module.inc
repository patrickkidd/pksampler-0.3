#include "pksampler.inc"
  
  




#declare PeakScale_Z = 3.1;
#declare PeakScale_X = .1;
#declare PeakScale_Y = .2;

#declare PeakYInset = .06;
       
#declare PeakNumSlots = 17;
#declare PeakSlotHeight = (PeakScale_Z / PeakNumSlots);


#declare T_Glass = texture {
   pigment { color red 1.0 green 1.0 blue 1.0 filter 0.95 }
   finish {
      ambient 0.0
      diffuse 0.0
      reflection 0.1
      phong 0.3
      phong_size 90
   }
}

#declare I_Glass4 =                  //Use with Top & Stem
   interior{
      ior 1.51
      caustics 2
      fade_distance 1.1
      fade_power 2
   }
       
       
#declare PeakModuleIndentShape = union {
        
    box { 
      1,-1
      scale <PeakScale_X, PeakScale_Y, PeakScale_Z>
      pigment { White }
   }
           
           
#local i=0;
#while(i<PeakNumSlots)
   box {
      <-(PeakScale_X*.9),-.1,-PeakScale_X>,
      <(PeakScale_X*.9),.5, PeakSlotHeight>
      translate <0,0,-PeakScale_Z+(i*(((PeakScale_Z-.05)*2)/PeakNumSlots))+ .32>
   }
#local i = i + 1;
#end         
   
   translate <0,-.201,0>
}
 
 
 
#declare PeakLEDBulb = light_source {
   0
   color Green  
   looks_like {
      box {
         <-PeakScale_X,-PeakScale_Y,-PeakScale_Z>,
         <PeakScale_X, .0001, PeakScale_Z>   
         
         pigment {
            gradient z
            color_map {
               [ 0 color <0,1.7,0>]
               [.3 color <1,1.7,0>]
               [.5 color <1.7,1.7,0>]
               [.8 color <1.7,0,0>]
            }
            scale 6.2
            translate -3.1
         }
      }
   }
} 
   
     
#declare PeakLED = difference {
   
   object {PeakLEDBulb }
   box {
      <PeakScale_X,0,PeakScale_Z+1>,
      <-PeakScale_X,PeakScale_Y,-PeakScale_Z>
      translate <0,0,PeakScale_Z * (clock/127) * 1.94> // a little adjustment at the end for high-end values
   }
   translate <0,-PeakYInset,.1>// a little adjustment at the end for low-end values
} 

/*
#declare PeakLED = difference {
   
   object {PeakLEDBulb }
   box {
      <PeakScale_X,0,PeakScale_Z+1>,
      <-PeakScale_X,PeakScale_Y,-PeakScale_Z>
      translate <0,0,PeakScale_Z * (clock/127) * 1.94> // a little adjust ment at the end for high-end values
   }
   translate <0,-PeakYInset,.1>// a little adjust ment at the end for low-end values
}
*/


  
// glass cover 
// needs better visibility, right now it just dims the colors
   
   /*
box {
   <PeakScale_X,-.001,PeakScale_Z>,
   <-PeakScale_X,PeakYInset,-PeakScale_Z>
   texture {T_Glass}
   finish { phong 1}
   interior{I_Glass4}
}
*/

     