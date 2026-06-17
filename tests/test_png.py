import struct
import unittest
import zlib

from procmount.png import encode_png


def _decode(data):
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    pos = 8
    width = height = None
    idat = b""
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos : pos + 4])
        tag = data[pos + 4 : pos + 8]
        body = data[pos + 8 : pos + 8 + length]
        crc = struct.unpack(">I", data[pos + 8 + length : pos + 12 + length])[0]
        assert crc == zlib.crc32(tag + body) & 0xFFFFFFFF, "bad CRC"
        if tag == b"IHDR":
            width, height = struct.unpack(">II", body[:8])
        elif tag == b"IDAT":
            idat += body
        pos += 12 + length
    raw = zlib.decompress(idat)
    stride = width * 3
    rows = [raw[i * (stride + 1) + 1 : i * (stride + 1) + 1 + stride] for i in range(height)]
    return width, height, b"".join(rows)


class TestPng(unittest.TestCase):
    def test_roundtrip(self):
        w, h = 4, 3
        pixels = bytes(range(w * h * 3))
        w2, h2, decoded = _decode(encode_png(w, h, pixels))
        self.assertEqual((w2, h2), (w, h))
        self.assertEqual(decoded, pixels)

    def test_signature(self):
        self.assertTrue(encode_png(1, 1, b"\x00\x00\x00").startswith(b"\x89PNG"))


if __name__ == "__main__":
    unittest.main()
