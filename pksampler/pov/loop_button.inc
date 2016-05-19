#include "button.inc"     
     

#declare Loop_X = .22;
#declare Loop_D = -50;
              
                            
#declare LoopArrow = union {


   difference {   
      
      torus {
         .22
         .05
      }

      box {
         <-.5,.2,0>,
         <.5,-.2,-.5>
      }
      box {
         <-.5,.2,0>,
         <.5,-.2,-.5>
         rotate y*Loop_D
      }
   
   }
   
   cylinder {
      <-Loop_X,0,0>,
      <-Loop_X-.1,0,.15>,
      .05
   }    
   
   cylinder {
      <-Loop_X,0,0>,
      <-.075,0,.05>,
      .05
   } 
   
         
   // head      
   sphere {
      <-Loop_X,0,0>,
      .05
   }      
   // arm
   sphere {
      <-Loop_X-.1,0,.15>,
      .05
   }    
   // tail
   sphere {
      0,
      .05
      translate <Loop_X, 0,0>
      rotate y*Loop_D
   }
   // inside
   sphere {
       <-.075,0,.05>,
       .05
   }
         
         
   finish { ambient .4 }
   translate <0,0,0>   
}


#declare LoopLabel = union {
   object {
      LoopArrow
      pigment { color <.8,.8,.8> } 
   }
   object {
      LoopArrow
      pigment { White }
      rotate y*180
   }
} 
                           
     
     
#macro DrawLoopButton(Color)

difference {
   DrawButton(Color)
   object {
      TranslateForButton(LoopLabel)
      translate <0,.19,0>
      scale <1.1,1,1>
   }
}

#end
