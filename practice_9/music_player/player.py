from pathlib import Path
import pygame


class MusicPlayer:
    SUPPORTED_EXTS = {".mp3", ".wav", ".ogg"}

    def __init__(self, music_dir: Path):
        pygame.mixer.init()
        self.music_dir = music_dir
        self.tracks: list[Path] = sorted(
            p for p in music_dir.iterdir()
            if p.is_file() and p.suffix.lower() in self.SUPPORTED_EXTS
        ) if music_dir.exists() else []
        self.index = 0
        self.is_playing = False

    @property
    def current_track(self) -> Path | None:
        if not self.tracks:
            return None
        return self.tracks[self.index]

    def play(self) -> None:
        track = self.current_track
        if not track:
            return
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.load(str(track))
            pygame.mixer.music.play()
        self.is_playing = True

    def stop(self) -> None:
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self) -> None:
        if not self.tracks:
            return
        self.index = (self.index + 1) % len(self.tracks)
        pygame.mixer.music.load(str(self.tracks[self.index]))
        pygame.mixer.music.play()
        self.is_playing = True

    def prev_track(self) -> None:
        if not self.tracks:
            return
        self.index = (self.index - 1) % len(self.tracks)
        pygame.mixer.music.load(str(self.tracks[self.index]))
        pygame.mixer.music.play()
        self.is_playing = True

    def get_position_sec(self) -> float:
        pos_ms = pygame.mixer.music.get_pos()
        return max(0.0, pos_ms / 1000.0)