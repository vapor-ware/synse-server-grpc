
build-hub:  ## Build the docker image for creating a new GitHub release
	docker build -f dockerfile/hub.dockerfile \
		-t vaporio/hub:latest \
		-t vaporio/hub:v2.3.0-pre10 .


release-github: build-hub  ## Create a new GitHub release with $PKG_VER as the version
	docker run -it -v $(PWD):/data vaporio/hub \
		release create -d \
		-a python/dist/synse_plugin-$(PKG_VER).tar.gz \
		-m "v$(PKG_VER)" v$(PKG_VER)


.PHONY: build-hub release-github