#include "button.inc"
#include "tap_button.inc"



#declare CueButtonZVal = .26;
#declare CueLabel = union {
   cylinder {
      <0,0,0>,
      <CueButtonZVal,0,CueButtonZVal>,
      .05
   }
   cylinder {
      <0,0,0>,
      <CueButtonZVal,0,-CueButtonZVal>,
      .05
   }
   cylinder {
      <-.15,0,CueButtonZVal*.5>,
      <-.15,0,-CueButtonZVal*.5>,
      .05
   }
      
   
   // roundies
   sphere {
      <0,0,0>,
      .05
   }
   sphere {
      <CueButtonZVal,0,CueButtonZVal>,
      .05
   }
   sphere {
      <CueButtonZVal,0,-CueButtonZVal>,
      .05
   }
   sphere {
      <-.15,0,CueButtonZVal*.5>,
      .05
   }
   sphere {
      <-.15,0,-CueButtonZVal*.5>,
      .05
   }
   
   pigment { White }
   finish { ambient .4 }
   scale <1,1.1,1>
   translate <0,.08,.03>
}

   
#declare Cue_X = .23;
#declare CueArrow = union {
   cylinder {
      <-Cue_X,0,-Cue_X>,
      <0,0,0>,
      .05
   }
   cylinder {
      <Cue_X,0,-Cue_X>,
      <0,0,0>,
      .05
   }
   sphere {
      <0,0,0>,
      .05
   }
   sphere {
      <-Cue_X,0,-Cue_X>,
      .05
   }
   sphere {
      <Cue_X,0,-Cue_X>,
      .05
   }
   pigment { White }
   finish { ambient .4 }
   scale <1,1.1,1>
}         

#macro DrawCueButton(Color)

difference {
   DrawTapButton(Color)
   TranslateForTapButton(CueLabel)
}                     
   
#end 


#declare CueUpLabel = union {
   // upper
   object {
      CueArrow
      translate <0,0,.23>
   }       
   // lower
   object {
      CueArrow
      translate <0,0,.0 >
   }
   translate <0,.2,0>
}   

#declare CueDownLabel = union {
   CueUpLabel
   rotate y*180
}


#macro DrawCueUpButton(Color)

difference {
   DrawButton(Color)
   TranslateForButton(CueUpLabel)
}                     
   
#end

#macro DrawCueDownButton(Color)

difference {
   DrawButton(Color)
   TranslateForButton(CueDownLabel)
}                     
   
#end          
