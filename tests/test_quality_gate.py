import numpy as np
import pytest
from PIL import Image, ImageFilter

from quality.gate import check, sharpness, to_grey

rng = np.random.default_rng(0)
TEXTURE = rng.integers(60, 200, size=(128, 128)).astype(np.float64)  # synthetic, sharp, mid-grey


def test_sharp_mid_grey_with_coin_passes():
    result = check(TEXTURE, coin_visible=True)
    assert result.image_ok and result.failed == []


def test_blur_lowers_sharpness_and_fails():
    blurred = np.asarray(Image.fromarray(TEXTURE.astype(np.uint8)).filter(ImageFilter.GaussianBlur(4)), dtype=float)
    assert sharpness(blurred) < sharpness(TEXTURE)
    assert "blurred" in check(blurred, coin_visible=True).failed


def test_flat_image_has_zero_sharpness():
    assert sharpness(np.full((32, 32), 128.0)) == 0


@pytest.mark.parametrize("level, reason", [(10, "too dark"), (250, "too bright")])
def test_exposure(level, reason):
    img = np.clip(TEXTURE - TEXTURE.mean() + level, 0, 255)
    assert reason in check(img, coin_visible=True).failed


@pytest.mark.parametrize("coin", [None, False])
def test_unconfirmed_coin_fails(coin):
    result = check(TEXTURE, coin_visible=coin)
    assert not result.image_ok and "coin not confirmed" in result.failed


def test_large_sharp_photo_is_not_called_blurred():
    """A sharp scene photographed at phone resolution must not fail just for being large (decision D8)."""
    small = Image.fromarray(TEXTURE.astype(np.uint8))
    phone = np.asarray(small.resize((3000, 3000), Image.Resampling.BICUBIC), dtype=np.float64)
    assert sharpness(phone) < 100  # raw measure collapses at high resolution
    assert "blurred" not in check(phone, coin_visible=True).failed


def test_small_images_are_measured_as_they_are():
    assert check(TEXTURE, coin_visible=True).sharpness == sharpness(TEXTURE)


def test_to_grey_reads_a_file(tmp_path):
    path = tmp_path / "x.png"
    Image.fromarray(TEXTURE.astype(np.uint8)).convert("RGB").save(path)
    assert to_grey(path).shape == (128, 128)
