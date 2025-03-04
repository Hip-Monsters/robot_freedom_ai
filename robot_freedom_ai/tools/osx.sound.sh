
import sounddevice as sd
sd.query_devices()
>>> import sounddevice as sd
>>> sd.query_devices()
  0 USBAudio2.0, Core Audio (0 in, 2 out)
< 1 USBAudio2.0, Core Audio (0 in, 2 out)
  2 USBAudio2.0, Core Audio (1 in, 0 out)
> 3 MacBook Pro Microphone, Core Audio (1 in, 0 out)
  4 MacBook Pro Speakers, Core Audio (0 in, 2 out)
>>>
https://apple.stackexchange.com/questions/452879/change-audio-input-and-output-devices-from-terminal
from  AppKit import NSSpeechSynthesizer
import os
os.system("SwitchAudioSource -a -f json")
os.system("SwitchAudioSource -c -f json")
nssp = NSSpeechSynthesizer
ve = nssp.alloc().init()
os.system("SwitchAudioSource -i 119")
ve.startSpeakingString_("hi")

os.cmd("SwitchAudioSource -i 109")
ve.startSpeakingString_("hi")

ve.startSpeakingString_("hi")
sd.default.device = [0,3]
sd.query_devices()


   python port_scan.py
 
   SwitchAudioSource -a -f json
   SwitchAudioSource -i 113
   python engine.py ./scripts/script_1.csv
   
   
   

   os.system("SwitchAudioSource -a -f json "  )
