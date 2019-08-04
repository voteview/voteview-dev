import functools
import typing as t

import attr


lock = functools.partial(attr, frozen=True, slots=True, cmp=False)

UNSET = "__UNSET__"


def asdict(obj: object) -> t.Dict[str, object]:
    return {k: v for k, v in attr.asdict() if v != UNSET}
