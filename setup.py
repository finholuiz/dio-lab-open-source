from setuptools import setup, find_packages

setup(
    name="simple_image_tools",
    version="0.1.0",
    author="Seu Nome",
    author_email="seuemail@example.com",
    description="Um pacote simples para processamento de imagens",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seuusuario/simple_image_tools",
    packages=find_packages(),
    install_requires=[
        "Pillow"
    ],
    python_requires=">=3.8",
)
