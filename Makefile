all: index.html

index.html: README.md kultiad.css
	pandoc README.md -s -c kultiad.css -o $@
