.PHONY: help install run test clean deploy

help:
	@echo "Nextia Content Automation - Commands"
	@echo "===================================="
	@echo "make install     - Instala dependencias"
	@echo "make run         - Ejecuta el sistema"
	@echo "make test        - Ejecuta tests"
	@echo "make clean       - Limpia archivos"
	@echo "make format      - Formatea código"

install:
	pip install -r requirements.txt

run:
	python main.py

test:
	pytest tests/ -v

format:
	black src/ tests/
	flake8 src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/

