from main import resumir

def test_corta_no_limite():
    assert resumir("um dois três", max_palavras=2) == "um dois"