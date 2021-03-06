OS=`uname -s`

build: clean
	@echo
	@echo "checking dependencies"
	@echo
	env
	docker version
	pip -V
	pip install -r tests/requirements.txt
	python setup.py install

gpu: build
	@if hash nvidia-docker 2>/dev/null; then \
		echo "nvidia-docker found"; \
		docker pull nvidia/cuda:8.0-runtime; \
	else \
		if [ "${OS}" = "Linux" ] ; then \
			if [ -f /etc/redhat-release ] ; then \
				wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker-1.0.1-1.x86_64.rpm && \
				sudo rpm -i /tmp/nvidia-docker*.rpm && rm /tmp/nvidia-docker*.rpm; \
				sudo systemctl start nvidia-docker; \
				docker pull nvidia/cuda:8.0-runtime; \
			elif [ -f /etc/debian_version ] ; then \
				wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1-1_amd64.deb && \
				sudo dpkg -i /tmp/nvidia-docker*.deb && rm /tmp/nvidia-docker*.deb; \
				docker pull nvidia/cuda:8.0-runtime; \
			else \
				wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1_amd64.tar.xz && \
				sudo tar --strip-components=1 -C /usr/bin -xvf /tmp/nvidia-docker*.tar.xz && rm /tmp/nvidia-docker*.tar.xz && \
				sudo -b nohup nvidia-docker-plugin > /tmp/nvidia-docker.log; \
				docker pull nvidia/cuda:8.0-runtime; \
			fi \
		else \
			echo "unable to install nvidia-docker on this host"; \
		fi \
	fi

clean:
	rm -rf .cache
	rm -rf .coverage
	rm -rf .vent
	rm -rf vent.egg-info
	rm -rf vent.iso
	rm -rf dist
	rm -rf build
	rm -rf plugins
	rm -rf core
	pip uninstall -y vent || true

test: build
	py.test -v --cov=. -k 'not vendor' --cov-report term-missing

.PHONY: build test
