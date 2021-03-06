#include "colors.inc" 
#include "pksampler.inc" 








# declare lit_segment = light_source
   {<0,0,0> color 1
   looks_like {
      union {
         sphere { <0,0,0> 0.8
              translate <0,-2.5,0> }
         sphere { <0,0,0> 0.8
              translate <0,2.5,0> }
         cylinder { <0,-2.5,0>, <0,2.5,0> ,0.8}
         pigment { color <0,.63,0> }
         finish { ambient 1 }
         }
     }
      rotate <90,0,0>
   }
     
     
# declare dark_segment =
      union {
         sphere { 
            <0,0,0> 0.8 
            translate <0,-2.5,0> 
         }
         sphere {
            <0,0,0> 0.8 
            translate <0,2.5,0> 
         }
         cylinder {
            <0,-2.5,0>,
            <0,2.5,0>,
            0.8
         }
         //pigment {Gray05} // looks good on black
         pigment { Gray65 }
         //color Gray
         finish { ambient .5 }
         rotate <90,0,0>
         scale <1,.05,1>
      }

/*
 aaa
b   c
b   c
 ddd
e   f
e   f
 ggg
*/
      
#macro led(a,b,c,d,e,f,g)

   union {
        
      object {
         #if(a != 0)
            lit_segment
         #else
            dark_segment
         #end
         rotate <0,90,0>      
         translate <0,0,7.4>}
      
      object {
         #if(b != 0)
            lit_segment 
         #else
            dark_segment
         #end
         translate <-3.6,0,3.7> }
      
      object {
         #if(c != 0)
            lit_segment
         #else
            dark_segment
         #end
         translate <3.6,0,3.7> }
         
      object {
         #if(d != 0)
            lit_segment     
         #else
            dark_segment
         #end
         rotate <0,90,0>}
      
      object { 
         #if(e != 0)
            lit_segment
         #else
            dark_segment 
         #end
         translate <-3.6,0,-3.7> }      
      
      object {
         #if(f != 0)
            lit_segment
         #else
            dark_segment
         #end
         translate <3.6,0,-3.7> }
         
      object { 
         #if(g != 0)
            lit_segment
         #else
            dark_segment
         #end
         rotate <0,90,0> 
         translate <0,0,-7.4>}
      
      scale <.1,.1,.1>
   }
#end


/*
 aaa
b   c
b   c
 ddd
e   f
e   f
 ggg
*/
#macro DrawNum(num)
   #switch(num)
      #case (0)
      led(1,1,1,0,1,1,1)
      #break
      #case (1)
      led(0,0,1,0,0,1,0)
      #break
      #case (2)
      led(1,0,1,1,1,0,1)
      #break
      #case (3)
      led(1,0,1,1,0,1,1)
      #break
      #case (4)
      led(0,1,1,1,0,1,0)
      #break
      #case (5)
      led(1,1,0,1,0,1,1)
      #break
      #case (6)
      led(1,1,0,1,1,1,1)
      #break
      #case (7)
      led(1,0,1,0,0,1,0)
      #break
      #case (8)
      led(1,1,1,1,1,1,1)
      #break
      #case (9)
      led(1,1,1,1,0,1,1)
      #break
      #case (10)
      led(0,0,0,0,0,0,0) // off
      #break
      #case(11)
      led(0,0,0,1,0,0,0) // minus
      #break
   #else
      led(0,0,0,0,0,0,0)
   #end
#end
             




/********************** 
   THE SCENE 
 **********************/
                       
#declare SCALE = .5;

PK_Light()
PK_Camera()
PK_Plane()
          

// THE Rim
          
#declare Z = .92;
#declare X = .6;
#declare R = .05;
#declare C = .1;
#declare Y = 4;

union {
   
union {
                      
cylinder {
  <-X,0,Z>,
  <X,0,Z>,
  R
  pigment { color C }
  scale <1,Y,1>
}
cylinder {
  <-X,0,-Z>,
  <X,0,-Z>,
  R
  pigment { color C }
  scale <1,Y,1>
}                 
cylinder {
  <-X, 0, Z>
  <-X, 0,-Z>,
  R
  pigment { color C }
  scale <1,Y,1>
}  
cylinder {
  <X, 0, -Z>,
  <X, 0, Z>,
  R
  pigment { color C }
  scale <1,Y,1>
}
 
 
DrawNum(clock) 



// The Back plate

box {
  <-X,.01,Z>,
  <X,-.01,-Z>
  pigment { color C }
}
 
 
  translate <-.02,0,0>
}

   scale <SCALE,SCALE*2,SCALE>
}

 
      
