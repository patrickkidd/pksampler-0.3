#include "mixerslider.inc"
#include "tap_button.inc"
#include "button.inc"
#include "reverb_knob.inc"
#include "delay_knob.inc"
#include "start_button.inc"
#include "cue_button.inc"
#include "pk_button.inc"
#include "pitch_button.inc"
#include "nudge_button.inc"
#include "pause_button.inc"
#include "loop_button.inc"



#declare Scene_Mixer_1_XOffset = -1.5;
#declare Scene_Mixer_1_Value = 1;
#declare Scene_Mixer_2_XOffset = 0;   
#declare Scene_Mixer_2_Value = 3;

#declare Scene_CueButton_XOffset = 2;
#declare Scene_CueButton_ZOffset = -1.9;
#declare Scene_StartButton_XOffset = 4;
#declare Scene_StartButton_ZOffset = -1.9;  
   
#declare Scene_PauseButton_XOffset = 2;
#declare Scene_PauseButton_ZOffset = -.2;
#declare Scene_LoopButton_XOffset = 4;
#declare Scene_LoopButton_ZOffset = -.2;

#declare Scene_NudgeUpButton_XOffset = 2;
#declare Scene_NudgeUpButton_ZOffset = 1.3;  
#declare Scene_NudgeDownButton_XOffset = 4;
#declare Scene_NudgeDownButton_ZOffset = 1.3;

#declare Scene_PitchUpButton_XOffset = 2;
#declare Scene_PitchUpButton_ZOffset = 2.6;  
#declare Scene_PitchDownButton_XOffset = 4;
#declare Scene_PitchDownButton_ZOffset = 2.6;

#declare Scene_ReverbKnob_XOffset = 1.9;
#declare Scene_ReverbKnob_ZOffset = 3.9;
#declare Scene_DelayKnob_XOffset = 3.9;
#declare Scene_DelayKnob_ZOffset = 3.9;

#declare Scene_TempoButton_XOffset = -1.1;
#declare Scene_TempoButton_ZOffset = 4.4;


#declare TrackFacePlate = difference {
   box {
      <-2.5,-.2,-3.5>,
      <5.1, 0, 12>
      pigment { White }
   }
           
   object {
      MixerIndentShape
      translate <Scene_Mixer_1_XOffset,0,0> 
   }    
   object {
      MixerIndentShape   
      translate <Scene_Mixer_2_XOffset,0,0>
   }
   object {
      TapButtonIndentShape
      translate <Scene_CueButton_XOffset, 0, Scene_CueButton_ZOffset>   
   } 
   object {
      TapButtonIndentShape
      translate <Scene_StartButton_XOffset, 0, Scene_StartButton_ZOffset>   
   }
   object {
      ButtonIndentShape
      translate <Scene_PauseButton_XOffset, 0, Scene_PauseButton_ZOffset>
   }
   object {
      ButtonIndentShape 
      translate <Scene_LoopButton_XOffset, 0, Scene_LoopButton_ZOffset>
   }
   object {
      ButtonIndentShape 
      translate <Scene_NudgeUpButton_XOffset, 0, Scene_NudgeUpButton_ZOffset>
   }  
   object {
      ButtonIndentShape 
      translate <Scene_NudgeDownButton_XOffset, 0, Scene_NudgeDownButton_ZOffset>
   }
   object {
      ButtonIndentShape 
      translate <Scene_PitchUpButton_XOffset, 0, Scene_PitchUpButton_ZOffset>
   }  
   object {
      ButtonIndentShape 
      translate <Scene_PitchDownButton_XOffset, 0, Scene_PitchDownButton_ZOffset>
   }
   object {
      KnobIndentShape
      translate <Scene_ReverbKnob_XOffset, 0, Scene_ReverbKnob_ZOffset>
   }
   object {
      KnobIndentShape
      translate <Scene_DelayKnob_XOffset, 0, Scene_DelayKnob_ZOffset>
   }
   object {
      ButtonIndentShape
      translate <Scene_TempoButton_XOffset, 0, Scene_TempoButton_ZOffset>
  }   
}


#declare TrackControls = union {
   object {
      MixerIndicator
      translate <Scene_Mixer_1_XOffset,0,0> 
   }    
   object {
      MixerIndicator   
      translate <Scene_Mixer_2_XOffset,0,0>
   }
   object {
      DrawCueButton(PKRed)
      translate <Scene_CueButton_XOffset, 0, Scene_CueButton_ZOffset>   
   } 
   object {
      DrawStartButton(PKGreen)
      translate <Scene_StartButton_XOffset, 0, Scene_StartButton_ZOffset>   
   }
   
   object {
      DrawPauseButton(PKBlue)
      translate <Scene_PauseButton_XOffset, 0, Scene_PauseButton_ZOffset>
   }
   
   object {
      DrawLoopButton(PKGreen) 
      translate <Scene_LoopButton_XOffset, 0, Scene_LoopButton_ZOffset>
   }
   
   object {
      DrawNudgeUpButton(PKRed) 
      translate <Scene_NudgeUpButton_XOffset, 0, Scene_NudgeUpButton_ZOffset>
   }  
   object {
      DrawNudgeDownButton(PKRed) 
      translate <Scene_NudgeDownButton_XOffset, 0, Scene_NudgeDownButton_ZOffset>
   }
   object {
      DrawPitchUpButton(PKRed) 
      translate <Scene_PitchUpButton_XOffset, 0, Scene_PitchUpButton_ZOffset>
   }  
   object {
      DrawPitchDownButton(PKRed) 
      translate <Scene_PitchDownButton_XOffset, 0, Scene_PitchDownButton_ZOffset>
   }
   object {
      union {
         DrawKnob()
         KnobLEDBulb
         ReverbKnobLabel
      }
      translate <Scene_ReverbKnob_XOffset, 0, Scene_ReverbKnob_ZOffset>
   } 
   
   object {
      union {
         DrawKnob()
         KnobLEDBulb
         DelayKnobLabel
      }
      translate <Scene_DelayKnob_XOffset, 0, Scene_DelayKnob_ZOffset>
   }
   object {
      DrawPKButton(PKBlue) 
      translate <Scene_TempoButton_XOffset, 0, Scene_TempoButton_ZOffset>
   }
}
