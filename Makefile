develop:
	pip install -r src/requirements/develop.pip

test:
	pytest tests

clean:
	@rm -fr dist/ ~build
	@rm -fr .cache .eggs


compile-requirements:
	pip install pip-tools devpi-builder
	@pip-compile src/requirements/install.in \
		--upgrade \
		--rebuild \
		--no-header \
		--no-emit-trusted-host \
		--no-index -o src/requirements/install.pip
	@pip-compile src/requirements/testing.in \
		src/requirements/install.pip \
		--upgrade \
		--rebuild \
		--no-header \
		--no-emit-trusted-host \
		--no-index -o src/requirements/testing.pip
	@pip-compile src/requirements/develop.in \
		src/requirements/testing.pip \
		--upgrade \
		--rebuild \
		--no-header \
		--no-emit-trusted-host \
		--no-index -o src/requirements/develop.pip

sync-requirements:
	pip-sync src/requirements/develop.pip


cache-requirements:
	pip install devpi-builder
	devpi-builder src/requirements/develop.pip  http://localhost:3141/sax/dev --user sax
