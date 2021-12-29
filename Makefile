.PHONY: start-dev build-prod frontend bootstrap clean lint test
.DEFAULT_GOAL := test

test: frontend lint
	@py.test test/ --cov=./app/main.py -s

lint:
	@flake8 .

clean:
	@find . -type f -name '*.pyc' -delete

bootstrap:
	@pip install -r requirements.txt
	@pip install -r requirements-test.txt
	@python setup.py develop
	@yarn install

build-prod: bootstrap
	@yarn webpack --mode production

start-dev:
	@yarn webpack --mode development --watch & ./venv/bin/python3 ./app/main.py

install: build-prod
	@mkdir -p /opt/IKEA-Notifier
	@cp -a ./app/* /opt/IKEA-Notifier
	@cp ikeanotifier.service /etc/systemd/system/ikeanotifier.service
	@systemctl enable ikeanotifier.service
	@systemctl start ikeanotifier.service

uninstall:
	systemctl stop ikeanotifier.service
	systemctl disable ikeanotifier.service
	@rm /etc/systemd/system/ikeanotifier.service
