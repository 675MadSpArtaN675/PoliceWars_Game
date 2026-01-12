from ...game_objects.abstract_objects import GameObject

from ..game_loop_controller import GameLoopController
from ..action_performer import ActionPerformer
from ..configurators.event_listeners_configurator import EventListenersConfigurator
from ..unit_control import UnitChooser


class GameCycleAdditionsConfigurator:
    _game_cycle: GameLoopController = None

    _chooser: UnitChooser = None
    _click_performer: ActionPerformer = None
    _ui_click_performer: ActionPerformer = None

    listeners: EventListenersConfigurator = None

    def __init__(
        self,
        game_cycle: GameLoopController,
        click_performer: ActionPerformer,
        ui_click_performer: ActionPerformer,
    ):
        self._game_cycle = game_cycle
        self._click_performer = click_performer
        self._ui_click_performer = ui_click_performer

    @property
    def chooser(self):
        return self._chooser

    @chooser.setter
    def chooser(self, chooser: UnitChooser):
        if chooser is not None:
            self._chooser = chooser

    def ConfigureChooser(self, policeman_patterns: list[GameObject]):
        if self._chooser is None:
            self._chooser = UnitChooser(policeman_patterns)

    def ConfigureEventListeners(self):
        self.listeners = EventListenersConfigurator(self._game_cycle)

        self.listeners.ConfigureEventListener()
        self.listeners.ConfigureKeyEventListener()
        self.listeners.ConfigureMouseEventListener(
            object_click_event=self._click_performer.perform,
            ui_click_event=self._ui_click_performer.perform,
        )
