from dataclasses import dataclass
from typing import Optional

@dataclass
class StealthConfig:
    languages: list = None
    vendor: str = "Google Inc."
    platform: str = "Win32"
    webgl_vendor: str = "Intel Inc."
    renderer: str = "Intel Iris OpenGL Engine"
    fix_hairline: bool = True

@dataclass
class DriverConfig:
    headless: bool = False
    user_agent: Optional[str] = None
    proxy: Optional[str] = None
    wait_time: int = 10
    window_size: tuple = (1920, 1080)
    disable_images: bool = False
    disable_javascript: bool = False

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

DEFAULT_STEALTH_CONFIG = StealthConfig(
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True
)