from typing import Optional

from core.agent import Agent
from core.config import Config
from core.llm import HelloAgentLLM


class SimpleAgent(Agent):
    def __init__(self,
         name: str,
         llm: HelloAgentLLM,
         system_prompt: Optional[str] = None,
         config: Optional[Config] = None,
         tool_registry: Optional['ToolRegistry'] = None,
         enable_tool_calling: bool = True
    ):
        super().__init__(name,llm, system_prompt, config)
        self.tool_registry = tool_registry
        self.enable_tool_calling = enable_tool_calling and tool_registry is not None
        print(f"{name} 初始化完成，工具调用:{'启用' if self.enable_tool_calling else '禁用'}")

    def run(self,input_text: str,**kwargs) -> str:
        """
        重写运行的方法,实现简单的对话逻辑，支持可选工具调用
        :param input_text:
        :param kwargs:
        :return:
        """
        print(f"{self.name} 正在处理： {input_text}")