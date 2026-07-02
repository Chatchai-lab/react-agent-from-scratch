from src.tools.base import ToolRegistry
from src.tools.calculator import calculator
from src.tools.web_search import web_search

registry = ToolRegistry([calculator, web_search])
