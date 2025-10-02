from __future__ import annotations

from io import BytesIO
from PIL import Image
from stegano import lsb


def hide_bytes_in_image(input_image_path: str, data: bytes, output_image_path: str) -> None:
	# stegano.lsb works with strings; we will hexlify-like via latin1-safe mapping
	payload = data.decode('latin1')
	secret = lsb.hide(input_image_path, payload)
	# Ensure save format is PNG to preserve lossless pixels
	secret.save(output_image_path, format="PNG")


def reveal_bytes_from_image(stego_image_path: str) -> bytes | None:
	payload = lsb.reveal(stego_image_path)
	if payload is None:
		return None
	return payload.encode('latin1')
# ...existing code from steganography_utils.py will be copied here