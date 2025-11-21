import time
from CoreAudio import (
    AudioObjectPropertyAddress,
    AudioObjectAddPropertyListenerBlock,
    kAudioObjectSystemObject,
    kAudioHardwarePropertyDevices,
)
import CoreAudio

def on_device_changed(self, args):
    print("Audio devices have changed!")
    # prase args
    print(args)

addr_devices = AudioObjectPropertyAddress(
    kAudioHardwarePropertyDevices,
    CoreAudio.kAudioObjectPropertyScopeGlobal,
    CoreAudio.kAudioObjectPropertyElementMain
)
AudioObjectAddPropertyListenerBlock(
    kAudioObjectSystemObject,
    addr_devices,
    None,
    on_device_changed
)

while True:
    time.sleep(1)