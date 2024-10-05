from dataclasses import dataclass, field

from kirin.interp.frame import Frame


@dataclass
class InterpreterState:
    frames: list[Frame] = field(default_factory=list)

    def push_frame(self, frame: Frame):
        self.frames.append(frame)
        return frame

    def pop_frame(self) -> Frame:
        return self.frames.pop()

    def current_frame(self) -> Frame:
        if not self.frames:
            raise ValueError(
                "unable to retrieve the current frame because no frames were pushed"
            )
        return self.frames[-1]

    def stacktrace(self) -> list[Frame]:
        return self.frames
