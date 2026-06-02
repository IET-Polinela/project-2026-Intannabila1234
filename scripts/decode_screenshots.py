import json
import pathlib
import base64

content_path = pathlib.Path(r'C:/Users/Lenovo/AppData/Roaming/Code/User/workspaceStorage/4e15aa691111b65a511f982ce0b4b209/GitHub.copilot-chat/chat-session-resources/2ca59ceb-a9d1-4a48-961d235873481d26/call_s3oM0ovlXl2zzx44wCqH9BfS__vscode-1780332641493/content.txt')
output_dir = pathlib.Path(r'C:/Users/Lenovo/Documents/npm24782077_iet_2026')

text = content_path.read_text(encoding='utf-8')
obj = json.loads(text[text.index('{'):])
for name, b64 in obj.items():
    out_path = output_dir / f'{name}.png'
    out_path.write_bytes(base64.b64decode(b64))
    print('wrote', out_path)
