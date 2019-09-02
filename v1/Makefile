.PHONY: build run

IMAGE=hr_leaderboard
VERSION=1.0.0
CONTAINER=hr_leaderboard
PORT=$(shell grep -w PORT hr_leaderboard.config | cut -d "=" -f2)

build:
	docker build -t $(IMAGE):$(VERSION) .

run:
	docker run -d \
	-p $(PORT):$(PORT) \
	--name $(CONTAINER) \
	$(IMAGE):$(VERSION)

clean:
	docker rm -f $(CONTAINER)

update:
	$(MAKE) build
