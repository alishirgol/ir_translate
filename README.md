# irtranslate

Simple Google Translate library without API key / کتابخانه ساده ترجمه بدون کلید API

## Sync Example
```python
from irtranslate import Translator
tr = Translator()
print(tr.translate("سلام دنیا", dest="en"))
