

.PHONY: build
build:
		@echo "Build image"
		docker build -t claudiojd/loboorganizado:latest -f django-docker/dockerfile.yml .



