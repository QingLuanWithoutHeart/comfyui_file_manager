import os
import shutil
from pathlib import Path
from typing import Any, Optional

class FileManager:
    """
    文件管理器节点: 可以移动或删除指定的文件。
    用于自动化流程中处理生成的中间文件或最终输出。
    现在支持作为中间节点使用，可接受任意输入，也可单独使用。
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": ""}),
                "operation": (["move", "delete"],),
            },
            "optional": {
                "input_data": ("ANY",),  # 改为可选
                "target_folder": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING", "ANY",)
    RETURN_NAMES = ("status", "input_data",)
    FUNCTION = "process"
    CATEGORY = "utils/FileManager"

    def process(
        self,
        file_path: str,
        operation: str,
        input_data: Any = None,
        target_folder: Optional[str] = None
    ):
        if input_data is None:
            input_data = {}

        file_path = os.path.expandvars(file_path)
        file_path = file_path.strip('"').strip("'")
        file_path_obj = Path(file_path)

        if not file_path_obj.exists():
            return (f"❌ 文件不存在: {file_path_obj}", input_data)

        try:
            if operation == "delete":
                file_path_obj.unlink()
                return (f"✅ 已删除: {file_path_obj}", input_data)

            elif operation == "move":
                if not target_folder:
                    return ("❌ 缺少目标文件夹", input_data)

                target_folder_obj = Path(os.path.expandvars(target_folder)).resolve()
                target_folder_obj.mkdir(parents=True, exist_ok=True)

                target_path = target_folder_obj / file_path_obj.name
                shutil.move(str(file_path_obj), str(target_path))
                return (f"✅ 已移动到: {target_path}", input_data)

        except Exception as e:
            return (f"❌ 操作失败: {str(e)}", input_data)

        return ("❌ 未知操作", input_data)

NODE_CLASS_MAPPINGS = {
    "FileManager": FileManager
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FileManager": "File Manager"
}
