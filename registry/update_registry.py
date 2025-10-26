#!/bin/env python3

import requests, os
from pathlib import Path

old: str = "old"
Path(old).mkdir(parents=True, exist_ok=True)

REGISTRY_LINKS: dict[str, str] = {
    "https://raw.githubusercontent.com/KhronosGroup/EGL-Registry/refs/heads/main/api/egl.xml": "egl.xml",
    "https://raw.githubusercontent.com/KhronosGroup/OpenGL-Registry/refs/heads/main/xml/gl.xml": "gl.xml",
    "https://raw.githubusercontent.com/KhronosGroup/OpenGL-Registry/refs/heads/main/xml/glx.xml": "glx.xml",
    "https://raw.githubusercontent.com/KhronosGroup/OpenGL-Registry/refs/heads/main/xml/wgl.xml": "wgl.xml",
}

# move the old files
for file in REGISTRY_LINKS.values():
    if os.path.exists(file):
        os.rename(file, os.path.join(old, file))
    else:
        print(f"{file} does not exist, skipping backup...")


# fetch the new files
for link, file in REGISTRY_LINKS.items():
    response = requests.get(link)
    response.raise_for_status()
    with open(file, "wb") as f:
        f.write(response.content)

print("registry updated")
