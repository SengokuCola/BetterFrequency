from typing import List, Tuple, Type, Any, Optional
from src.plugin_system import (
    BasePlugin,
    register_plugin,
    BaseCommand,
    ComponentInfo,
    ConfigField
)
from src.plugin_system.apis import send_api, frequency_api


class SetFocusValueCommand(BaseCommand):
    """设置当前聊天的focus_value值"""
    command_name = "set_focus_value"
    command_description = "设置当前聊天的focus_value值：/chat focus_value <数字> 或 /chat f <数字>"
    command_pattern = r"^/chat\s+(?:focus_value|f)\s+(?P<value>[+-]?\d*\.?\d+)$"

    async def execute(self) -> Tuple[bool, Optional[str], bool]:
        try:
            # 获取命令参数 - 使用命名捕获组
            if not self.matched_groups or "value" not in self.matched_groups:
                return False, "命令格式错误", False
            
            value_str = self.matched_groups["value"]
            if not value_str:
                return False, "无法获取数值参数", False
            
            value = float(value_str)
            
            # 获取聊天流ID
            if not self.message.chat_stream or not hasattr(self.message.chat_stream, "stream_id"):
                return False, "无法获取聊天流信息", False
            
            chat_id = self.message.chat_stream.stream_id
            
            # 设置focus_value
            frequency_api.set_focus_value_adjust(chat_id, value)
            
            # 发送反馈消息（不保存到数据库）
            await send_api.text_to_stream(
                f"已设置当前聊天的focus_value调整值为: {value}",
                chat_id,
                storage_message=False
            )
            
            return True, None, False
            
        except ValueError:
            error_msg = "数值格式错误，请输入有效的数字"
            await self.send_text(error_msg, storage_message=False)
            return False, error_msg, False
        except Exception as e:
            error_msg = f"设置focus_value失败: {str(e)}"
            await self.send_text(error_msg, storage_message=False)
            return False, error_msg, False


class SetTalkFrequencyCommand(BaseCommand):
    """设置当前聊天的talk_frequency值"""
    command_name = "set_talk_frequency"
    command_description = "设置当前聊天的talk_frequency值：/chat talk_frequency <数字> 或 /chat t <数字>"
    command_pattern = r"^/chat\s+(?:talk_frequency|t)\s+(?P<value>[+-]?\d*\.?\d+)$"

    async def execute(self) -> Tuple[bool, Optional[str], bool]:
        try:
            # 获取命令参数 - 使用命名捕获组
            if not self.matched_groups or "value" not in self.matched_groups:
                return False, "命令格式错误", False
            
            value_str = self.matched_groups["value"]
            if not value_str:
                return False, "无法获取数值参数", False
            
            value = float(value_str)
            
            # 获取聊天流ID
            if not self.message.chat_stream or not hasattr(self.message.chat_stream, "stream_id"):
                return False, "无法获取聊天流信息", False
            
            chat_id = self.message.chat_stream.stream_id
            
            # 设置talk_frequency
            frequency_api.set_talk_frequency_adjust(chat_id, value)
            
            # 发送反馈消息（不保存到数据库）
            await send_api.text_to_stream(
                f"已设置当前聊天的talk_frequency调整值为: {value}",
                chat_id,
                storage_message=False
            )
            
            return True, None, False
            
        except ValueError:
            error_msg = "数值格式错误，请输入有效的数字"
            await self.send_text(error_msg, storage_message=False)
            return False, error_msg, False
        except Exception as e:
            error_msg = f"设置talk_frequency失败: {str(e)}"
            await self.send_text(error_msg, storage_message=False)
            return False, error_msg, False


class ShowFrequencyCommand(BaseCommand):
    """显示当前聊天的频率控制状态"""
    command_name = "show_frequency"
    command_description = "显示当前聊天的频率控制状态：/chat show 或 /chat s"
    command_pattern = r"^/chat\s+(?:show|s)$"

    async def execute(self) -> Tuple[bool, Optional[str], bool]:
        try:
            # 获取聊天流ID
            if not self.message.chat_stream or not hasattr(self.message.chat_stream, "stream_id"):
                return False, "无法获取聊天流信息", False
            
            chat_id = self.message.chat_stream.stream_id
            
            # 获取当前频率控制状态
            current_focus_value = frequency_api.get_current_focus_value(chat_id)
            current_talk_frequency = frequency_api.get_current_talk_frequency(chat_id)
            focus_value_adjust = frequency_api.get_focus_value_adjust(chat_id)
            talk_frequency_adjust = frequency_api.get_talk_frequency_adjust(chat_id)
            
            # 构建显示消息
            status_msg = f"""当前聊天频率控制状态
Focus Value (专注值):
   • 当前值: {current_focus_value:.2f} (x {focus_value_adjust:.2f})

Talk Frequency (发言频率):
   • 当前值: {current_talk_frequency:.2f} (x {talk_frequency_adjust:.2f})

使用命令:
   • /chat focus_value <数字> 或 /chat f <数字> - 设置专注值调整
   • /chat talk_frequency <数字> 或 /chat t <数字> - 设置发言频率调整
   • /chat show 或 /chat s - 显示当前状态"""
            
            # 发送状态消息（不保存到数据库）
            await send_api.text_to_stream(status_msg, chat_id, storage_message=False)
            
            return True, None, False
            
        except Exception as e:
            error_msg = f"获取频率控制状态失败: {str(e)}"
            # 使用内置的send_text方法发送错误消息
            await self.send_text(error_msg, storage_message=False)
            return False, error_msg, False


# ===== 插件注册 =====


@register_plugin
class BetterFrequencyPlugin(BasePlugin):
    """BetterFrequency插件 - 控制聊天频率的插件"""

    # 插件基本信息
    plugin_name: str = "better_frequency_plugin"
    enable_plugin: bool = True
    dependencies: List[str] = []
    python_dependencies: List[str] = []
    config_file_name: str = "config.toml"

    # 配置节描述
    config_section_descriptions = {
        "plugin": "插件基本信息",
        "frequency": "频率控制配置"
    }

    # 配置Schema定义
    config_schema: dict = {
        "plugin": {
            "name": ConfigField(type=str, default="better_frequency_plugin", description="插件名称"),
            "version": ConfigField(type=str, default="1.0.0", description="插件版本"),
            "enabled": ConfigField(type=bool, default=True, description="是否启用插件"),
        },
        "frequency": {
            "default_focus_adjust": ConfigField(type=float, default=0.0, description="默认focus_value调整值"),
            "default_talk_adjust": ConfigField(type=float, default=0.0, description="默认talk_frequency调整值"),
            "max_adjust_value": ConfigField(type=float, default=10.0, description="最大调整值"),
            "min_adjust_value": ConfigField(type=float, default=-10.0, description="最小调整值"),
        }
    }

    def get_plugin_components(self) -> List[Tuple[ComponentInfo, Type]]:
        return [
            (SetFocusValueCommand.get_command_info(), SetFocusValueCommand),
            (SetTalkFrequencyCommand.get_command_info(), SetTalkFrequencyCommand),
            (ShowFrequencyCommand.get_command_info(), ShowFrequencyCommand),
        ]
