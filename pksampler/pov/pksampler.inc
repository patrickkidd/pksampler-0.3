#include "colors.inc"
                        
                        
#declare ReallyRed = color <1.3,.45,.45>;
#declare ReallyGreen = color <.25,1.1,.25>;
#declare ReallyBlue = color <.45,.45,1.1>;
                        
#declare PKRed = color <1.2,.6,.6>;
#declare PKGreen = color <.6,1,.6>;
#declare PKBlue = color <.6,.6,1.1>;
#declare PKBlack = color <.4,.4,.4>;
#declare PKGrey = color <.6,.6,.6>;
                        
#declare PK_IndicatorWidth = .12;
#declare PK_CourseWidth = .07;
#declare PK_FineWidth = .05;

// camera
#macro PK_Camera()
   camera {
      location <0, 15, 0> // original
      //location <-1,3,-2>
      //location <-7,1,0>
      look_at 0
      angle 36
   }
#end

// light
#macro PK_Light()
   light_source { 
      <-600, 900, 600>
      color White
      area_light <700, 0, 0>, <0, 0, 700>, 8, 8
      fade_distance 100
   }
#end

#macro PK_Plane()
   plane {
      y, 0
      pigment { White }
   }
#end
    
#macro PK_OuterPlane()    
   plane {
      y, 0
      pigment { color <.8,.8,.8> }
   }                  
#end
   