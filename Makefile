# set up dev environment, WIP
dev:
	poetry install

build:
	poetry build

test:
	poetry run pytest	-v
