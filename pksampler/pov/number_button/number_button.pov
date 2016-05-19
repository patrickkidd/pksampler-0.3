#include "number_button.inc"


PK_Camera()
PK_Light()

difference {
   PK_OuterPlane()
   ButtonIndentShape
}
  

DrawNumberButton(ButtonClockedColor())

   