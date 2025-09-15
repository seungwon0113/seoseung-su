

# Create your tests here.
def add(a: int, b: int) -> int:
    return a + b

def test_add() -> None:
    add(1, 2)
    assert add(1, 2) == 3