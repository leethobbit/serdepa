"""test_serdepa.py: Tests for serdepa packets. """

import unittest

from serdepa import SerdepaPacket

from ctypes import c_uint8, c_uint32, c_int32


__author__ = "Raido Pahtma, ..."
__license__ = "MIT"


class PointStruct(SerdepaPacket):
    _fields_ = [
        ("x", c_int32),
        ("y", c_int32)
    ]


class OnePacket(SerdepaPacket):
    _fields_ = [
        ("header", c_uint8),
        ("timestamp", c_uint32),
        ("length", c_uint8, "len(data)"),
        ("data", c_uint8, "list"),
        ("tail", c_uint8, "list")
    ]


class AnotherPacket(SerdepaPacket):
    _fields_ = [
        ("header", c_uint8),
        ("timestamp", c_uint32),
        ("origin", PointStruct),
        ("points", c_uint8, "len(data)"),
        ("data", PointStruct, "list")
    ]

class ArrayPacket(SerdepaPacket):
    _fields_ = [
        ("header", c_uint8),
        ("data", PointStruct, "array(4)")
    ]


class TransformTester(unittest.TestCase):
    p1 = "010000303904010203040506"

    def test_one(self):
        p = OnePacket()
        p.header = 1
        p.timestamp = 12345
        p.data.append(1)
        p.data.append(2)
        p.data.append(3)
        p.data.append(4)
        p.tail.append(5)
        p.tail.append(6)

        self.assertEqual(p.serialize(), self.p1)

    def test_two(self):
        p = OnePacket()
        p.deserialize(self.p1)

        self.assertEqual(p.header, 1)
        self.assertEqual(p.timestamp, 12345)
        self.assertEqual(p.length, 4)
        self.assertEqual(len(p.data), 4)
        self.assertEqual(len(p.tail), 2)
        self.assertEqual(p.data, [1, 2, 3, 4])
        self.assertEqual(p.tail, [5, 6])


if __name__ == '__main__':
    unittest.main()