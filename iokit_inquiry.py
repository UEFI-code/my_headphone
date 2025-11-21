import ctypes
from ctypes import c_uint32, c_void_p, POINTER
from ctypes.util import find_library

iokit = ctypes.CDLL(find_library("IOKit"))

iokit.IOServiceMatching.restype = c_void_p
iokit.IOServiceGetMatchingServices.argtypes = [c_void_p, c_void_p, POINTER(c_void_p)]
iokit.IOServiceGetMatchingServices.restype = c_uint32
iokit.IOIteratorNext.argtypes = [c_void_p]
iokit.IOIteratorNext.restype = c_void_p
iokit.IOObjectRelease.argtypes = [c_void_p]

matching_dict = iokit.IOServiceMatching(b"IOAudioDevice")
iterator = c_void_p()
kr = iokit.IOServiceGetMatchingServices(None, matching_dict, ctypes.byref(iterator))
if kr != 0: raise RuntimeError("IOServiceGetMatchingServices failed")

print(iterator)
while True:
    device = iokit.IOIteratorNext(iterator)
    if not device: break
    print("Found device:", device)
    iokit.IOObjectRelease(device)

iokit.IOObjectRelease(iterator)