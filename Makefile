REGION?=us-west-2
CHECKS?=all

install:
	pipenv install

prometheus: EXTRA_ARGS?="--disable-duration-metrics"
prometheus: install
	pipenv run aws-quota-checker prometheus-exporter --region $(REGION) $(EXTRA_ARGS) $(CHECKS)

check: install
	pipenv run aws-quota-checker check --region $(REGION) $(CHECKS)

update_descriptions: install
	pipenv run python tools/update_descriptions.py 

