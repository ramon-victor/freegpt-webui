from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name="freeGPT",
    version="1.1.5",
    description="freeGPT is a Python package that gives free access to GPT3 and GPT4 and more models.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Ruu3f/freeGPT",
    author="Ruu3f",
    license="GPLv3",
    keywords=[
        "artificial-intelligence",
        "machine-learning",
        "ai-models",
        "chatllama",
        "gpt4free",
        "freegpt",
        "chatgpt",
        "python",
        "alpaca",
        "openai",
        "gpt3",
        "gpt4",
        "gpt",
        "py",
        "ai",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(),
    install_requires=[
        "pydantic",
        "pymailtm",
        "curl_cffi",
        "requests",
        "fake-useragent",
    ],
    project_urls={
        "Source": "https://github.com/Ruu3f/freeGPT",
        "Issues": "https://github.com/Ruu3f/freeGPT/issues",
    },
)
