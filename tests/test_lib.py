import os

from binypt import Binypt


def test_functionality():
    binypt_obj = Binypt("BTCUSDT", "3d", "01/01/2023-00:00:00", "01/03/2023-00:00:00")
    assert type(binypt_obj) is Binypt, "object could not be initialized"
    del binypt_obj


def test_exporting():
    binypt_obj = Binypt("BTCUSDT", "3d", "01/01/2023-00:00:00", "01/03/2023-00:00:00")
    output_path = "test_file.csv"
    with open(output_path, "w") as test_file:
        binypt_obj.export(test_file, "csv")
    assert (
        os.path.exists(output_path) is True and os.path.getsize(output_path) != 0
    ), "test file could not be written"
    os.remove("test_file.csv")
    del binypt_obj
