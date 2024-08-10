.PHONY: dev
dev:
	poetry install

.PHONY: build
build:
	poetry build

.PHONY: test
test:
	poetry run pytest	-v


# visual integration tests

test-segmentation:
	pf segment -f ./tests/data/videos/jupiter.mp4

test-stabilization:
	pf stabilize -f ./tests/data/videos/jupiter.mp4

test-quality:
	pf quality -f ./tests/data/videos/jupiter.mp4


# dev purposes only

# puppet cli task
puppet:
	poetry run pf puppet -f ./tests/data/videos/jupiter.mp4

# running a script currently in development
script:
	poetry run python ./scripts/build_reference_frame.py
