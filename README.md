# simple_image_tools

Um pacote simples de processamento de imagens em Python.

## Instalação

```bash
pip install simple_image_tools
```

## Exemplo de uso

```python
from simple_image_tools import resize_image, to_grayscale, blur_image

resize_image("input.jpg", "resized.jpg", (200, 200))
to_grayscale("input.jpg", "gray.jpg")
blur_image("input.jpg", "blur.jpg", radius=5)
```
