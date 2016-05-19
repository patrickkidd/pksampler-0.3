// mixerslider.inc
// all the fixins for creating mixer slider objects
   
      
         
#include "pksampler.inc"

/*
The slider is 30x190
*/

#declare NumCourse = 2;
#declare NumFine = 10;
#declare GrooveHeight = 3.1;
#declare GrooveWidth = .3;
#declare GrooveDepth = .07;

#declare GripSplines = 20;
#declare GripSplinesInc = (360/GripSplines);

#declare CourseTick = union {
   cylinder {
      <.1, 0, 0>, 
      <-.1, 0, 0>,
      PK_CourseWidth
   }
   sphere {
      <.1, 0, 0>
      PK_CourseWidth
   }
   sphere {
      <-.1, 0, 0>
      PK_CourseWidth
   }
   pigment { White }
}

#declare FineTick = union {
   /*
   cylinder {
      <.01, 0, 0>, 
      <-.01, 0, 0>, 
      FineWidth
   }
*/
   sphere {
      <.1, 0, 0>,
      PK_FineWidth
   }
   sphere {
      <-.1, 0, 0>,
      PK_FineWidth
   }
   pigment { White }
}



// ETCH-A-GRIP!      

#declare Grip = union{
   
   cylinder {
      <-1, .6, 0>
      <1, .6, 0>,
      .5
      
      pigment { White }
   } 

 
   #declare I=0;
   #while(I < GripSplines)
   cylinder {
      <-1, 0, -.5>
      <1, 0, -.5>
      .035
      pigment { color <1.5,1.5,1.5> } 
      rotate x*-(GripSplinesInc*I)
      #declare I = I + 1;  
      translate<0,.6,0>
   }             
   #end 
   scale <1,1,1.2>

}    
      

               
#declare MixerGrooveIndentShape = superellipsoid {
   <.1, .1>
   scale <.4, GrooveDepth, GrooveHeight>
   //pigment { color <.9 * (clock/127),1,1> }
   pigment {
      /*
      gradient z
      color_map {
         [ 0.0 color <0,1,0> ]
         [ 1.0 color ]
      }
      scale 6.5
      translate <0,0,-3.1>
      */
      White
   } // pigment
}


// THE GROOVEY-GROOVE-GROOVE
#declare MixerGrooveSlitShape =    
   box {
      <-.05, -.2, GrooveHeight-.45>,
      <.05 1, -GrooveHeight+.45>
      pigment { Black }
   }


#declare MixerIndentShape = union {
   object { MixerGrooveIndentShape }
   object { MixerGrooveSlitShape }
}


// THE INDICATOR
    
#declare MixerIndicator = difference {
   superellipsoid {
      <.3, .2>
      scale <.4, .3, .7>
   }          
   Grip
   pigment { White }
   finish { phong 1 }
   #declare GrooveRange = GrooveHeight-.8; 
   translate <0,0,(GrooveRange*2) * (clock / 127.0) - GrooveRange>
}


/*
// BIG TICKS
#local i = 0;
#while(i <= NumCourse)
  object {
    CourseTick
    scale <2,1,1>
    translate <0, -.05, i * ((GrooveHeight*2) / NumCourse) - GrooveHeight>
  }
  #local i = i + 1;
#end


  
// SMALL TICKS  
#local i = 0;
#while(i <= NumFine)
  object {
    FineTick
    scale <2.5,1,1>
    translate <0, -.05, i * ((GrooveHeight*2) / NumFine) - GrooveHeight>
  }
  #local i = i + 1;
#end
 */