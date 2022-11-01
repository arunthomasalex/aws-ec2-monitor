edit:
	@rm -rf dist
	@python -m build

test:
	@-mkdir .tmp
	@cd .tmp && python -m unittest discover ../app/tests -s ../ -v
	@rm -rf .tmp