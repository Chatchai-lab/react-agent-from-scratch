from src.tools.calculator import calculator


def test_addition():
    assert calculator.run({"expression": "2 + 2"}) == "4"


def test_operator_precedence():
    assert calculator.run({"expression": "12 * (3 + 4)"}) == "84"


def test_integer_division_formatted_without_decimal():
    assert calculator.run({"expression": "10 / 2"}) == "5"


def test_division_by_zero():
    result = calculator.run({"expression": "1 / 0"})
    assert "Fehler" in result


def test_invalid_syntax():
    result = calculator.run({"expression": "2 +"})
    assert "Fehler" in result


def test_rejects_unsafe_expression():
    result = calculator.run({"expression": "__import__('os').system(\"ls\")"})
    assert "Fehler" in result
