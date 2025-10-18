

def test_invalid_input(monkeypatch):
    inputs = iter(["x", "w"])  # first invalid, then valid
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = UserInputManager.input_safeguard(["w","a","s","d"], "x")
    assert result == "w"