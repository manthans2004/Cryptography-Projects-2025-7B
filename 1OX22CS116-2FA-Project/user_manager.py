from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

USER_DATA_DIR = Path("user_data")
USER_DB_FILE = USER_DATA_DIR / "user_data.json"


@dataclass
class UserProfile:
	username: str
	stego_image_path: str
	secret_coordinates: Dict[str, float]  # {"x": 0.45, "y": 0.62}
	decoy_images: List[str]


def ensure_user_storage() -> None:
	USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
	if not USER_DB_FILE.exists():
		USER_DB_FILE.write_text(json.dumps({}, indent=2))


def load_user_db() -> Dict[str, Dict]:
	ensure_user_storage()
	with USER_DB_FILE.open("r", encoding="utf-8") as f:
		return json.load(f)


def save_user_db(db: Dict[str, Dict]) -> None:
	USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
	with USER_DB_FILE.open("w", encoding="utf-8") as f:
		json.dump(db, f, indent=2)


def get_user(username: str) -> Optional[UserProfile]:
	db = load_user_db()
	data = db.get(username)
	if not data:
		return None
	return UserProfile(
		username=username,
		stego_image_path=data["stego_image_path"],
		secret_coordinates=data["secret_coordinates"],
		decoy_images=data["decoy_images"],
	)


def save_user_profile(profile: UserProfile) -> None:
	db = load_user_db()
	db[profile.username] = {
		"stego_image_path": profile.stego_image_path,
		"secret_coordinates": profile.secret_coordinates,
		"decoy_images": profile.decoy_images,
	}
	save_user_db(db)


def get_or_create_user_directory(username: str) -> Path:
	user_dir = USER_DATA_DIR / username
	user_dir.mkdir(parents=True, exist_ok=True)
	return user_dir
# ...existing code from user_manager.py will be copied here