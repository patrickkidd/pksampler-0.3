#include "main_zone_button.inc"

PK_Camera()
PK_Light()

difference {
   PK_Plane()
   ButtonIndentShape
}
         
DrawMainZoneButton(ButtonClockedColor())