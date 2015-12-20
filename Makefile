all: index.html

index.html: index.md kultiad.css
	pandoc index.md -s -c kultiad.css -o $@
