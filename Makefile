run:
	@echo "Inicializando servidor de desenvolvimento..."
	@trap 'kill 0' SIGINT; \
	python manage.py runserver 0.0.0.0:8000 & \
	npm run watch

check:
	@echo "Realizando checagem..."
	@python manage.py check ; \
	@ruff check . ; \
	@ruff format --check

test:
	@echo "Executando testes..."
	@python manage.py test

normalize: format fix

format:
	@echo "Formatando projeto..."
	@ruff format

fix:
	@echo "Arrumando erros indicandos pelo ruff..."
	@ruff check --fix
