from app.tools.python_executor import execute_python

def test_python_execution():
    code = """
        x = 10
        y = 20
        result = x + y
        """
    output = execute_python(code)

    assert "result" in output