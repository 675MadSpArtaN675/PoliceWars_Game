from .mouse_button import MouseButton
from .key_event import KeyEvent

from typing import Callable
from pygame.event import Event

EventListenerFunction = Callable[[Event], None]

__all__ = ["MouseButton", "KeyEvent", "EventListenerFunction"]
