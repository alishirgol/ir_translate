import asyncio
from irtranslate import Translator

tr = Translator()

# Sync
res1 = tr.translate(["سلام دنیا", "hi"], dest=["en", "tr"])
print(res1)
# Async
import asyncio
async def main():
    res_async = await tr.translate(["سلام دنیا", "hi"], dest=["en", "tr"])
    print(res_async)

asyncio.run(main())
