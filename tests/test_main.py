from binypt import Binypt
import pytest

def test_main_ability():
    binypt_obj = Binypt("BTCUSDT", "3d", "01/01/2022-00:00:00", "01/01/2023-00:00:00", "test.csv")
    assert type(binypt_obj) == Binypt