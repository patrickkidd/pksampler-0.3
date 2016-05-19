#include "pksampler.inc"

//tick marks
#declare CourseRes = 45;
#declare FineRes = 15;
// start/stop degrees. '0' is down
#declare MinValue = 45;
#declare MaxValue = 315;
#declare Radius = .5;
#declare YOffset = .05;

#declare ClockPercent = clock / 127;
#declare Increment = (MaxValue - MinValue) / 127;

#macro Course(deg)
   union {
      cylinder { 
         <0, 0, -Radius>, 
         <0, 0, -(Radius + .4)>, // adjust for length
         PK_CourseWidth
      }
      sphere {
         <0, 0, -(Radius + .4)>,
         PK_CourseWidth
      }
      pigment { color rgb<.7,.7,.7> }
      rotate y * deg
   }
#end
#macro Fine(deg) 
   sphere {
      <0, 0, -(Radius + .3)>
      PK_FineWidth
      pigment { color rgb<1,1,1> } 
      rotate y * deg 
   }
#end

PK_Camera()
PK_Light()
PK_Plane()


union {

   // the ring
   torus {
      Radius,
      PK_IndicatorWidth
      pigment { White }
      translate <0,YOffset,0>
   }

   // the indicator
   cylinder {
      <0,.4,0>
      //<(Radius * .75),.1,0>,
      <Radius, YOffset , 0>
      PK_IndicatorWidth
   }
   sphere {
      <0,1,0>, PK_IndicatorWidth
   }
   sphere {
      //<(Radius * .75),.1,0>, IndicatorWidth
      <Radius,YOffset ,0>, PK_IndicatorWidth
   }
   #if(clock != 0)
      rotate y*((MinValue+90) + (clock * Increment))
   #else
      rotate y*135
   #end
   texture {
      pigment { 
         color <(1-ClockPercent), (1-ClockPercent), (1-ClockPercent)>
      }
   }
   /*
   finish {
      ambient 1
   }
*/
}


// Course TICKS

#local deg = MinValue - CourseRes;
#while(deg < MaxValue)
  #local deg = deg + MinValue;
  Course(deg)
#end

// Fine TICKS

#local deg = MinValue - FineRes;
#while(deg < MaxValue)
  #local deg = deg + FineRes;
  Fine(deg)
#end
