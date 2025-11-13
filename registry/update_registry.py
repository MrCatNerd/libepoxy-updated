#!/bin/env python3

import aiohttp, asyncio, os
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
async def update_registry(session, link, file):
    async with session.get(link) as response:
        response.raise_for_status()
        content = await response.read()
        with open(file, "wb") as f:
            f.write(content)


async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            *[
                update_registry(session, link, file)
                for link, file in REGISTRY_LINKS.items()
            ]
        )


asyncio.run(main())

print("registry updated")
