edit:
	@rm -rf dist
	@python -m build

test:
	@-mkdir .tmp
	@cd .tmp && python -m unittest discover ../tests -s ../ -v
	@rm -rf .tmp