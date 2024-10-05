from dataclasses import dataclass, field


@dataclass
class RewriteResult:
    terminated: bool = field(default=False, kw_only=True)
    has_done_something: bool = field(default=False, kw_only=True)
    exceeded_max_iter: bool = field(default=False, kw_only=True)
