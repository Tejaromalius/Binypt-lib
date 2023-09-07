import binypt
import pytest

def test_main_ability():
    binypt_obj = binypt.Binypt("BTCUSDT", "3d", "01/01/2022-00:00:00", "01/01/2023-00:00:00", "test.csv", "resources/.metadata.json")
    assert type(binypt_obj) == binypt.Binypt