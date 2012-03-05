NAME = iprediaos-i2psnark-tools

VERSION := $(shell awk '/Version:/ { print $$2 }' $(NAME).spec)
RELEASE := $(shell awk '/Release:/ { print $$2 }' $(NAME).spec | sed 's|%{?dist}||g')
TAG=$(NAME)-$(VERSION)-$(RELEASE)

tag:
	@git tag -a -f -m "Tag as $(TAG)" -f $(TAG)
	@echo "Tagged as $(TAG)"

install: 
	@install -D i2psnark.desktop ${DESTDIR}/usr/share/applications/i2psnark.desktop
	@install -m 755 i2psnark-tool ${DESTDIR}/usr/bin/i2psnark-tool

archive: tag
	@git archive --format=tar --prefix=$(NAME)-$(VERSION)/ HEAD > $(NAME)-$(VERSION).tar
	@bzip2 -f $(NAME)-$(VERSION).tar
	@echo "$(NAME)-$(VERSION).tar.bz2 created"

clean:
	rm -f *~ *bz2
