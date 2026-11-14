
import runpy
import sys
import types


EXPECTED_COLORS = {
    "Pink": "#e2979c",
    "Green": "#9bdeac",
    "Blue": "#1f75fe",
    "Yellow": "#ffcc00",
    "Purple": "#b19cd9",
}

WIDGET_NAMES = [
    "window",
    "canvas",
    "label",
    "tick_label",
    "work_label",
    "break_label",
]


class FakeWidget:
    def __init__(self):
        self.config_calls = []

    def config(self, **kwargs):
        self.config_calls.append(kwargs)

    def __getattr__(self, name):
        return lambda *args, **kwargs: None


class FakeVariable:
    def __init__(self):
        self.value = "Pink"

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


def load_module():
    fake_tkinter = types.ModuleType("tkinter")
    fake_tkinter.__all__ = [
        "Tk", "Canvas", "Label", "Button", "Entry",
        "StringVar", "OptionMenu", "Toplevel",
        "NORMAL", "DISABLED"
    ]

    fake_tkinter.Tk = lambda *a, **k: FakeWidget()
    fake_tkinter.Canvas = lambda *a, **k: FakeWidget()
    fake_tkinter.Label = lambda *a, **k: FakeWidget()
    fake_tkinter.Button = lambda *a, **k: FakeWidget()
    fake_tkinter.Entry = lambda *a, **k: FakeWidget()
    fake_tkinter.StringVar = lambda *a, **k: FakeVariable()
    fake_tkinter.OptionMenu = lambda *a, **k: FakeWidget()
    fake_tkinter.Toplevel = lambda *a, **k: FakeWidget()
    fake_tkinter.NORMAL = "normal"
    fake_tkinter.DISABLED = "disabled"
    fake_tkinter.mainloop = lambda *args, **kwargs: None

    fake_tkinter.__all__ += ["mainloop"]


    original_tkinter = sys.modules.get("tkinter")
    sys.modules["tkinter"] = fake_tkinter

    try:
        namespace = runpy.run_path("Pomodoro (tkinter).py")
    finally:
        if original_tkinter is None:
            sys.modules.pop("tkinter", None)
        else:
            sys.modules["tkinter"] = original_tkinter

    return namespace


def test_all_supported_colors():
    namespace = load_module()

    for selected, expected in EXPECTED_COLORS.items():
        namespace["bg_color_var"].value = selected

        result = namespace["change_background"]()

        assert result is None
        for widget_name in WIDGET_NAMES:
            widget = namespace[widget_name]
            assert widget.config_calls[-1] == {"bg": expected}


def test_unknown_color_uses_pink_fallback():
    namespace = load_module()
    namespace["bg_color_var"].value = "Unknown"

    result = namespace["change_background"]()

    assert result is None
    for widget_name in WIDGET_NAMES:
        assert namespace[widget_name].config_calls[-1] == {
            "bg": "#e2979c"
        }


def test_twenty_argument_combinations():
    namespace = load_module()
    original_colors = namespace["bg_colors"].copy()

    cases = [
        (), (1,), ("x",), (None,), (True,),
        (1, 2), ("a", "b"), (None, None),
        (True, False), (0, 0), (1, 2, 3),
        ("a", "b", "c"), (None, 1, "x"),
        (False, False, False), (1, 2, 3, 4),
        ("pink", "green", "blue", "yellow", "purple"),
        (None, None, None, None, None),
        (True, 1, "x", None), (0, "0", False, True),
        ("extra", "arguments", "are", "ignored", "!"),
    ]

    namespace["bg_color_var"].value = "Blue"

    for args in cases:
        result = namespace["change_background"](*args)

        assert result is None
        for widget_name in WIDGET_NAMES:
            assert namespace[widget_name].config_calls[-1] == {
                "bg": "#1f75fe"
            }

    assert namespace["bg_colors"] == original_colors


if __name__ == "__main__":
    test_all_supported_colors()
    test_unknown_color_uses_pink_fallback()
    test_twenty_argument_combinations()
    print("All 3 background test groups passed!")
