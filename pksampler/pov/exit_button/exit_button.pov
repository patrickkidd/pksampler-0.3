#include "exit_button.inc"


PK_Camera()
PK_Light()
   
   

difference {
   PK_OuterPlane()
   object {
      ButtonIndentShape
      scale <1,1,1.5>
   }
}

DrawExitButton(ButtonClockedColor())

