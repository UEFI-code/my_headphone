import ctypes
from ctypes import c_void_p, POINTER
from ctypes.util import find_library

iokit = ctypes.CDLL(find_library("IOKit"))

iokit.IORegistryGetRootEntry.restype = c_void_p
iokit.IORegistryGetRootEntry.argtypes = [c_void_p]

iokit.IORegistryEntryGetChildIterator.restype = ctypes.c_uint32
iokit.IORegistryEntryGetChildIterator.argtypes = [c_void_p, c_void_p, POINTER(c_void_p)]

iokit.IOIteratorNext.argtypes = [c_void_p]
iokit.IOIteratorNext.restype = c_void_p

iokit.IORegistryEntryGetName.restype = ctypes.c_uint32
iokit.IORegistryEntryGetName.argtypes = [c_void_p, ctypes.c_char_p]

iokit.IOObjectRelease.argtypes = [c_void_p]

def traverse(node, plane=b"IOService", depth=0):
    buf = ctypes.create_string_buffer(128)
    iokit.IORegistryEntryGetName(node, buf)
    print("  " * depth + buf.value.decode())
    del buf

    iterator = c_void_p()
    kr = iokit.IORegistryEntryGetChildIterator(node, plane, ctypes.byref(iterator))
    if kr != 0 : return
    while True:
        child = iokit.IOIteratorNext(iterator)
        if not child: break
        traverse(child, plane, depth + 1)
        iokit.IOObjectRelease(child)
    iokit.IOObjectRelease(iterator)

root = iokit.IORegistryGetRootEntry(None)
traverse(root)
iokit.IOObjectRelease(root)