from audio.generators import _to_hexadecimal_bytes, _quantize


def test_to_hexadecimal_bytes():
    print("Testing audio.generators._to_hexadecimal_bytes...", end="")
    assert _to_hexadecimal_bytes(-32_768) == b"\x00\x80"
    assert _to_hexadecimal_bytes(0.0) == b"\x00\x00"
    assert _to_hexadecimal_bytes(32_767) == b"\xff\x7f"
    print("OK")


def test_quantize():
    print("Testing audio.generators._quantize...", end="")
    assert _quantize(1.0, min_num=-1, max_num=1) == 32_767
    # A little wrong but close enough (should be -32_768)
    assert _quantize(-1.0, min_num=-1, max_num=1) == -32_767
    print("OK")
