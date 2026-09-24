from typing import Optional

from core.agent import Agent
from core.config import Config
from core.llm import HelloAgentLLM
from core.message import Message


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

    def run(self,input_text: str,max_tool_iterations: int = 3,**kwargs) -> str:
        """
        重写运行的方法,实现简单的对话逻辑，支持可选工具调用
        :param input_text:
        :param kwargs:
        :return:
        """
        print(f"{self.name} 正在处理： {input_text}")

        #构建消息列表
        messages = []

        #添加系统消息 可能包含工具信息
        enhanced_system_prompt = self._get_enhanced_system_prompt()
        messages.append({"role":"system","content":enhanced_system_prompt})

        #添加历史对话
        for msg in self._history:
            messages.append({"role":msg.role,"content":msg.content})

        #添加当前用户信息
        messages.append({"role":"user","content":input_text})

        #如果没有启用工具调用，使用简单对话逻辑
        if not self.enable_tool_calling:
            response = self.llm.invok(messages,**kwargs)
            self.add_message(Message(input_text,"user"))
            self.add_message(Message(response,"assistant"))
            print(f"{self.name} 响应完成")
            return response

        #支持多轮工具调用的逻辑
        return self._run_with_tools(messages,input_text,max_tool_iterations,**kwargs)


    def _get_enhanced_system_prompt(self) -> str:
        """构建增强系统的提示词，包含工具信息"""


    def _run_with_tools(self,messages: list,input_text: str,max_tool_iterations: int,**kwargs):
        """支持工具调用的运行逻辑"""