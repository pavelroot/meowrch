import random
import logging
import subprocess
from PIL import Image
from pathlib import Path
import multiprocessing as mp
from dataclasses import dataclass
from typing import List, Optional, Dict

from .schemes import Theme
from vars import (
	MEOWRCH_ASSETS, ROFI_SELECTING_THEME, 
	WALLPAPERS_CACHE_DIR, THEMES_CACHE_DIR
)


@dataclass
class RofiResponse:
	exit_code: int
	selected_item: Optional[str]


class Selector:
	@staticmethod
	def _create_thumbnail(image_path: Path, thumbnail_path: Path):
		if thumbnail_path.exists():
			return

		# Проверяем, является ли файл видео
		video_extensions = {'.mp4', '.webm', '.avi', '.mov', '.mkv', '.gif'}
		is_video = image_path.suffix.lower() in video_extensions

		if is_video:
			# Для видео создаем превью с помощью ffmpeg
			try:
				subprocess.run([
					'ffmpeg', '-i', str(image_path),
					'-vf', 'scale=500:500:force_original_aspect_ratio=decrease,pad=500:500:(ow-iw)/2:(oh-ih)/2',
					'-frames:v', '1',
					'-y', str(thumbnail_path)
				], check=True, capture_output=True)
			except subprocess.CalledProcessError:
				# Если ffmpeg не работает, создаем простую иконку
				cls._create_video_icon(thumbnail_path)
		else:
			# Для изображений используем стандартный метод
			try:
				image = Image.open(image_path)
				width, height = image.size

				if width <= 500 and height <= 500:
					image.save(thumbnail_path)
					return

				if width > height:
					new_height = 500
					new_width = int(width * 500 / height)
				else:
					new_width = 500
					new_height = int(height * 500 / width)

				img = image.resize((new_width, new_height))
				img = img.crop((new_width // 2 - 500 // 2, new_height // 2 - 500 // 2, new_width // 2 + 500 // 2, new_height // 2 + 500 // 2))
				img.save(thumbnail_path)
			except Exception:
				# Если не удается открыть изображение, создаем иконку
				cls._create_video_icon(thumbnail_path)

	@staticmethod
	def _create_video_icon(thumbnail_path: Path):
		"""Создает простую иконку для видеофайла"""
		icon = Image.new('RGB', (500, 500), color='#1e1e2e')
		icon.save(thumbnail_path)

	@classmethod
	def _generate_rofi_list(cls, elements: Dict[str, Path], cache_dir: Path, random_el_text: str) -> list[str]:
		"""
		args:
			elements: Словарь, в котором ключ - заголовок, а значение - путь к иконке.
			cache_dir: Path - Путь до папки, в которую будут кэшироваться изображения
		"""

		cache_dir.mkdir(parents=True, exist_ok=True)
		rofi_list = [f"{random_el_text}\x00icon\x1f{str(MEOWRCH_ASSETS / 'random.png')}"]

		image_paths = []
		thumbnails = []

		for name, icon in elements.items():
			if icon.is_file():
				thumbnail = cache_dir / f"{icon.stem}.png"
				thumbnails.append(thumbnail)
				image_paths.append(icon)

		with mp.Pool(processes=4) as pool:
			pool.starmap(cls._create_thumbnail, zip(image_paths, thumbnails))

		for name, icon, thumbnail in zip(elements.keys(), elements.values(), thumbnails):
			if thumbnail.is_file():
				rofi_list.append(f"{name}\x00icon\x1f{str(thumbnail)}")

		return rofi_list

	@classmethod
	def _selection(cls, title: str, input_list: list, override_theme: str = None) -> RofiResponse:
		command = ["rofi", "-dmenu", "-i", "-p", title, "-theme", str(ROFI_SELECTING_THEME)]

		if override_theme is not None:
			command.extend(["-theme-str", override_theme])

		selection = subprocess.run(
			command,
			input="\n".join(input_list), 
			capture_output=True, 
			text=True
		)

		return RofiResponse(
			exit_code=selection.returncode,
			selected_item=selection.stdout.strip().split("\x00")[0]
		)

	@classmethod
	def select_wallpaper(cls, theme: Theme, video_mode: bool = False) -> Optional[Path]:
		if video_mode and hasattr(theme, 'available_videos') and theme.available_videos:
			elements: Dict[str, Path] = {video.name: video for video in theme.available_videos}
			title = "Choose a video wallpaper:"
			random_text = "Random Video"
			available_items = theme.available_videos
		else:
			elements: Dict[str, Path] = {wall.name: wall for wall in theme.available_wallpapers}
			title = "Choose a wallpaper:"
			random_text = "Random Wallpaper"
			available_items = theme.available_wallpapers

		response = cls._selection(
			title=title,
			input_list=cls._generate_rofi_list(
				elements=elements,
				cache_dir=WALLPAPERS_CACHE_DIR,
				random_el_text=random_text
			)
		)

		if response.exit_code != 0:
			logging.debug("The selection has been canceled")
			return None

		if response.selected_item == random_text:
			return random.choice(available_items)
		
		selection_path = next((p for p in available_items if p.name == response.selected_item), None)

		if selection_path is not None:
			return selection_path

		logging.debug("The item is not selected")
		return None

	@classmethod
	def select_theme(cls, all_themes: List[Theme]) -> None:
		elements: Dict[str, Path] = {theme.name: theme.icon for theme in all_themes}

		response = cls._selection(
			title="Choose a theme:",
			input_list=cls._generate_rofi_list(
				elements=elements,
				cache_dir=THEMES_CACHE_DIR,
				random_el_text="Random Theme",
			)
		)

		if response.exit_code != 0:
			logging.debug("Theme selection has been canceled")
			return None

		if response.selected_item == "Random Theme":
			return random.choice(all_themes)
		
		theme_selection = next((th for th in all_themes if th.name == response.selected_item), None)

		if theme_selection is not None:
			return theme_selection

		logging.debug("Theme is not selected")
		return None
