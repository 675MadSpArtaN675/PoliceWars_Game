from dataclasses import dataclass

from .mouse_button import MouseButton


@dataclass
class KeyEvent:
    event_type: int
    button: MouseButton | int

    def to_tuple(self):
        return (self.event_type, self.button)
