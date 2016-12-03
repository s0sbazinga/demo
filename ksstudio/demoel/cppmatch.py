# from ctypes import *
import ctypes


def main():
    # INTP = ctypes.POINTER(ctypes.c_int)
    # num = ctypes.c_int(42)
    # addr = ctypes.addressof(num)
    # print 'address:', addr, type(addr)
    # ptr = ctypes.cast(addr, INTP)
    # print 'pointer:', ptr
    # print 'value:', ptr[0]

    dll = ctypes.CDLL('pyext.dll')
    # cstr = ctypes.cast('TTT', ctypes.c_char_p)
    cstr = ctypes.c_char_p('TTT')
    tmp = ctypes.cast(cstr, ctypes.POINTER(ctypes.c_char))

    print cstr
    print type(cstr)
    cstr = dll.hello(cstr)
    cstr = ctypes.cast(cstr, ctypes.c_char_p)
    print cstr
    print type(cstr)
    print cstr.value

if __name__ == '__main__':
    main()
