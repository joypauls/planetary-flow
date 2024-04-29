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
	pf segment -f ./test/data/videos/jupiter.mp4

test-stabilization:
	pf stabilize -f ./test/data/videos/jupiter.mp4

