markdown="../sbse14.wiki"

commit:
	- git status
	- git commit -am "stuff"
	- git push origin master

update:
	- git pull origin master

status:
	- git status

markup:
	@$(foreach  f, $(shell ls *.py), bash py2md $f ; )

publish: markup
	cd $(markdown); git add *py.md; make commit

files:
	@echo "# Code:"
	@$(foreach  f, $(shell ls *.py), echo "+ [[$f]]: $f"; )

