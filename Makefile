
build:
	python -m build

test-upload:
	python -m twine upload --repository testpypi dist/* --skip-existing --verbose

upload:
	python -m twine upload dist/* --skip-existing --verbose
