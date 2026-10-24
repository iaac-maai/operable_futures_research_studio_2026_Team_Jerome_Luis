import csv

from PIL import Image

from pilot.prepare import prepare

GPS_TAG = 0x8825


def test_prepare_strips_metadata_and_renames(tmp_path):
    src = tmp_path / "phone"
    src.mkdir()
    exif = Image.Exif()
    exif[0x010F] = "PhoneMaker"  # camera make
    exif[GPS_TAG] = {1: "N", 2: (41.0, 23.0, 0.0)}  # synthetic GPS position
    Image.new("RGB", (40, 30), "grey").save(src / "IMG_1234.jpg", exif=exif)
    Image.new("RGB", (40, 30), "white").save(src / "IMG_1235.png")
    (src / "notes.txt").write_text("not a photo")

    out = tmp_path / "pilot" / "photos"
    index = prepare(src, out)

    assert [n for n, _ in index] == ["P0001.jpg", "P0002.jpg"]
    with Image.open(out / "P0001.jpg") as img:
        assert len(img.getexif()) == 0
        assert img.size == (40, 30)
    rows = list(csv.DictReader((tmp_path / "pilot" / "photo_index.csv").open()))
    assert rows[0] == {"photo_id": "P0001", "original_name": "IMG_1234.jpg"}
