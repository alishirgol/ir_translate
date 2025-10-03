import requests
import aiohttp
import asyncio
from time import sleep
from .exceptions import TranslationError, NetworkError, EmptyTextError

class Translator:
    BASE_URL = "https://translate.googleapis.com/translate_a/single"

    def __init__(self, default_dest="en", retries=3, delay=1, cache_enabled=True):
        self.default_dest = default_dest
        self.retries = retries
        self.delay = delay
        self.cache_enabled = cache_enabled
        self._cache = {}

    def translate(self, text, src="auto", dest=None, return_detected_lang=False):
        """
        متن یا لیست متن‌ها رو ترجمه کن.
        اگر await شود، async خواهد بود.
        اگر معمولی صدا زده شود، sync ران می‌شود.
        """
        if asyncio.get_event_loop().is_running():
            # در حالت async
            return self._translate_async(text, src, dest, return_detected_lang)
        else:
            # در حالت sync
            return asyncio.run(self._translate_async(text, src, dest, return_detected_lang))

    async def _translate_async(self, text, src="auto", dest=None, return_detected_lang=False):
        dest = dest or self.default_dest

        if isinstance(text, list):
            return [await self._translate_item(t, src, dest, return_detected_lang) for t in text]
        return await self._translate_item(text, src, dest, return_detected_lang)

    async def _translate_item(self, text, src, dest, return_detected_lang=False):
        if isinstance(dest, list):
            results = {}
            for d in dest:
                results[d] = await self._translate_single(text, src, d, return_detected_lang)
            return results
        return await self._translate_single(text, src, dest, return_detected_lang)

    async def _translate_single(self, text, src, dest, return_detected_lang=False):
        if isinstance(text, str) and not text.strip():
            raise EmptyTextError("متن خالی است / Empty text")
        if isinstance(text, list) and all(not t.strip() for t in text):
            raise EmptyTextError("متن خالی است / Empty text")

        cache_key = (str(text), src, str(dest))
        if self.cache_enabled and cache_key in self._cache:
            return self._cache[cache_key]

        q = text if isinstance(text, str) else "\n".join(text)
        params = {"client": "gtx", "sl": src, "tl": dest, "dt": "t", "q": q}

        for attempt in range(1, self.retries + 1):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.BASE_URL, params=params, timeout=10) as resp:
                        if resp.status != 200:
                            raise NetworkError(f"HTTP {resp.status}")
                        data = await resp.json()
                        
                        # ✅ بررسی داده برگشتی
                        if not data or not isinstance(data, list) or not data[0]:
                            raise TranslationError("Translation returned empty or invalid data")
                        
                        translated_lines = []
                        for item in data[0]:
                            if item and item[0]:
                                translated_lines.append("".join(item[0]))
                        
                        translated = "\n".join(translated_lines)
                        detected = data[2] if len(data) > 2 else src
                        result = {"translation": translated, "detected_lang": detected} if return_detected_lang else translated
                        
                        if self.cache_enabled:
                            self._cache[cache_key] = result
                        return result
            except Exception as e:
                if attempt == self.retries:
                    raise TranslationError(f"Translation failed: {e}")
                await asyncio.sleep(self.delay)
