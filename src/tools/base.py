from abc import ABC, abstractmethod

from google.genai import types


class Tool(ABC):
    name: str
    description: str
    parameters: dict

    @abstractmethod
    def run(self, args: dict) -> str:
        ...

    def to_function_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=self.parameters,
        )


class ToolRegistry:
    def __init__(self, tools: list[Tool]):
        self._tools = {tool.name: tool for tool in tools}

    def as_gemini_tool(self) -> types.Tool:
        return types.Tool(
            function_declarations=[t.to_function_declaration() for t in self._tools.values()]
        )

    def get(self, name: str) -> Tool:
        return self._tools[name]
