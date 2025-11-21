import ctypes
from ctypes import c_uint32, c_void_p, POINTER, byref
from ctypes.util import find_library

coreaudio = ctypes.CDLL(find_library("CoreAudio"))

AudioObjectID = c_uint32
kAudioObjectSystemObject = AudioObjectID(0)

# Property address struct
class AudioObjectPropertyAddress(ctypes.Structure):
    _fields_ = [("mSelector", c_uint32),
                ("mScope", c_uint32),
                ("mElement", c_uint32)]

# Constants (from CoreAudio headers)
kAudioHardwarePropertyDevices = 0x64657673  # 'devs'
kAudioObjectPropertyScopeGlobal = 0x676C6F62  # 'glob'
kAudioObjectPropertyElementMaster = 0

addr = AudioObjectPropertyAddress(
    mSelector=kAudioHardwarePropertyDevices,
    mScope=kAudioObjectPropertyScopeGlobal,
    mElement=kAudioObjectPropertyElementMaster
)

size = c_uint32(0)
coreaudio.AudioObjectGetPropertyDataSize(
    kAudioObjectSystemObject,
    byref(addr),
    0,
    None,
    byref(size)
)
print("Size of device data:", size.value)

num_devices = size.value // ctypes.sizeof(AudioObjectID)
devices = (AudioObjectID * num_devices)()
coreaudio.AudioObjectGetPropertyData(
    kAudioObjectSystemObject,
    byref(addr),
    0,
    None,
    byref(size),
    devices
)

print("Audio devices IDs:", list(devices))