# imageViewer
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.14.2-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/wingdingg27-glitch/image-viewer/tests)

Простое приложение для просмотра изображений с возможностью обрезки и сохранения. Разработано на Python с использованием PyQt6
## Возможности:
- открытие папок и отдельных изображений
- обрезка и сохранение изображений
- навигация между изображениями с зацикливанием
- масштабирование изображений
- поддерживает форматы jpg, jpeg, png, bmp, webp, bmp, gif
- изменение размера окна
- покрытие unit-тестами
## Используемые технологии:
- **Python** 3.14.2
- **PyQt6** - графический интерфейс
- **PyTest** - тестирование
- **PyInstaller** - сборка приложения
## Установка и запуск:
```bash
#клонируйте репозиторий
git clone https://github.com/wingdingg27-glitch/imageViewer.git
#создайте и активируйте виртуальное окружение
python -m venv venv
venv/Scripts/activate #для Windows
#установите зависимости
pip install -r requirements.txt
#запустите приложение
python app.py
