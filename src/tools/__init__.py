from src.tools.base import ToolRegistry
from src.tools.calculator import calculator
from src.tools.file_system import read_file, write_file
from src.tools.web_search import web_search

registry = ToolRegistry([calculator, web_search, read_file, write_file])
