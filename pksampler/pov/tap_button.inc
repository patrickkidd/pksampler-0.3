
#include "button.inc"


// COLORS:
// Red: 0-2
// Green: 3-5
// Blue:  6-8
   


#declare Round = 0.25;    
            
   // button    
#macro DrawTapButton(Color)
union {
   
   // flat segment
   superellipsoid { 
      <Round, Round-0.15> 
      scale <.8, .45, .45>
   } 

   // tilted segment
   superellipsoid { 
      <Round, Round-0.15> 
      //scale <ButtonShapeXScale, .45, .45>
      scale <ButtonShapeXScale, .45, .45>
      rotate x*-15
      translate <0,-.0882,-.67>
   }                      
   #if(clock >= 0 & clock < 3)
      #declare ElseClock = clock;
   #end
   #if(clock >= 3 & clock < 6 )
      #declare ElseClock = clock - 3;
   #end
   #if(clock >= 6)     
      #declare ElseClock = clock - 6;
   #end           
   pigment { Color }
   translate <0,-.2+(-.2*ElseClock),.07*ElseClock>
   rotate x*(15*(ElseClock/2))
   finish { phong 1 }
   scale <1,1,.95>
   translate <0,0,.02>
   //finish { ambient .1 }
}
#end


#declare TapButtonIndentShape = superellipsoid { 
   <.05,.08>           
   scale <ButtonIndentXScale, 4, .84>
   pigment { color <.9,.9,.9> }
   translate <0,0,-.345>
}


#macro TranslateForTapButton(O)
   object {
      O
      translate <0,.2+(-.2*ElseClock),.07*ElseClock>
      rotate x*(15*(ElseClock/2))
   }
#end


