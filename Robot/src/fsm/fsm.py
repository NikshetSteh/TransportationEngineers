from fsm.context import Context
from fsm.state import State


class FSM:
    def __init__(
            self,
            context: Context,
            start_state: State = None,
    ):
        self.current_state = start_state
        if start_state is not None:
            start_state.start(self)
        self.context = context

    def change_state(self, new_state: State) -> None:
        if self.current_state is not None:
            self.current_state.stop()
        self.current_state = new_state
        if new_state is not None:
            new_state.start(self)
