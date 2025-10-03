class TranslationError(Exception):
    """❌ خطا در فرآیند ترجمه / Translation process error"""
    pass

class NetworkError(TranslationError):
    """⚠️ خطای شبکه / Network-related error"""
    pass

class EmptyTextError(TranslationError):
    """📄 متن خالی است / Text is empty"""
    pass
