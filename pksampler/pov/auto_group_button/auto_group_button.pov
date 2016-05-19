#include "auto_group_button.inc"

          
PK_Camera()
PK_Light()

difference {
   PK_OuterPlane()
   ButtonIndentShape
}
                
DrawAutoGroupButton(ButtonClockedColor())                
