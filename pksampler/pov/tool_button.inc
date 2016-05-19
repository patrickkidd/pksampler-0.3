#include "button.inc"     
     


#declare ToolLabel = union {

   difference {
     union {
         cylinder {
            <0,0,0>,
            <0,1,0>,
            .25
         }
         box {
            <0,0,-.25>,
            <1,1,.25>
         }
         cylinder {
            <1,-.05,0>,
            <1,1,0>,
            .4
            pigment { Grey }
            finish { ambient .6}
         }
      }
      box {
         <.95,-0.1,-.19>,
         <1.5,1.1,.19>
      }
   }
     
   pigment { White }
   finish { ambient .4 }
   translate <-.5,.2,-0.1>
   scale <.5,.5,.5>
   rotate y*-15
   rotate x*5
}
                           
     
     
#macro DrawToolButton(Color)

difference {
   DrawButton(Color)
   TranslateForButton(ToolLabel)
}

#end


