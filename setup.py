from setuptools import setup, find_packages

setup(
    name="irtranslate",
    version="1.0.4",
    author="Ali Shirgol",
    author_email="ali.shirgol.coder@gmail.com",
    description="یک کتابخانه ترجمه ساده با تشخیص زبان / Simple translation library with auto language detection",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alishirgol",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.1",
        "aiohttp>=3.8.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
    ],
)
