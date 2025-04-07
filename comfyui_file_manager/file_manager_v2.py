import os
import shutil
from typing import Any

class FileManagerV2:
    """File Manager V2: 支持复制、移动、删除文件。文件不存在时跳过。输出详细状态信息，支持任意类型数据传递。"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": ""}),
                "operation": (["move", "copy", "delete"],),
                "destination_path": ("STRING", {"default": "", "multiline": False}),
            },
            "optional": {
                "in_data": ("ANY",),  # 可选输入，支持任意类型
            }
        }

    RETURN_TYPES = ("ANY", "STRING",)
    RETURN_NAMES = ("out_data", "status_info",)
    FUNCTION = "process"
    CATEGORY = "utils/FileManager"

    def process(self, file_path: str, operation: str, destination_path: str, in_data: Any = None):
        file_path = file_path.strip().strip('"').strip("'")
        destination_path = destination_path.strip().strip('"').strip("'")

        file_name = os.path.basename(file_path)

        if not os.path.exists(file_path):
            status = f"File not found: {file_path} (skipped)"
            print(f"[FileManagerV2] {status}")
            return (in_data, status)

        try:
            if operation == "move":
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                shutil.move(file_path, destination_path)
                status = f"Moved {file_name} → {destination_path}"
            elif operation == "copy":
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                shutil.copy(file_path, destination_path)
                status = f"Copied {file_name} → {destination_path}"
            elif operation == "delete":
                os.remove(file_path)
                status = f"Deleted {file_name}"
            else:
                status = f"Unknown operation: {operation}"

            print(f"[FileManagerV2] {status}")
            return (in_data, status)

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"[FileManagerV2] {error_msg}")
            return (in_data, error_msg)


NODE_CLASS_MAPPINGS = {
    "FileManagerV2": FileManagerV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FileManagerV2": "🧾 File Manager v2"
}
