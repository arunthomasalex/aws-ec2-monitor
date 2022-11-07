edit: clean
	@python -m build

clean:
	@rm -rf dist

test:
	@-mkdir .tmp
	@cd .tmp && python -m unittest discover ../tests -s ../ -v
	@rm -rf .tmp