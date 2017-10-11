_MODULE=python-broadlink
PREFIX = $(DESTDIR)/usr
INSTALL = /bin/install -c
MKDIR = /bin/install -c -d
RM = rm -rf
CP = cp -a
LN = ln -s
TAR = $(shell which tar)
TMPDIR := $(shell mktemp -d)
CURRENT_DIR := $(shell pwd)
PKG_MGR := $(shell which yum)
RPMBUILD := $(shell which rpmbuild)
PYTHON := $(shell which python3) 

install:
	pushd ./src
	$(PYTHON) setup --root $(DESTDIR)

rpm:
	$(TAR) \
		cvfz $(TMPDIR)/$(_MODULE).tar.gz \
		--transform 's,^,$(_MODULE)/,' \
	       	--exclude=.git \
		--exclude=.gitignore \
		--exclude='*.swp' \
		--exclude=.rpmbuild \
		--exclude=$(_MODULE).tar.gz \
		./
	mkdir -p .rpmbuild/SPEC .rpmbuild/SOURCES .rpmbuild/SRPMS .rpmbuild/RPMS .rpmbuild/BUILD .rpmbuild/BUILDROOT
	mv $(TMPDIR)/$(_MODULE).tar.gz .rpmbuild/SOURCES
	$(RPMBUILD) -tb --define "_topdir $(CURRENT_DIR)/.rpmbuild" .rpmbuild/SOURCES/$(_MODULE).tar.gz
	$(RPMBUILD) -ta --define "_topdir $(CURRENT_DIR)/.rpmbuild" .rpmbuild/SOURCES/$(_MODULE).tar.gz

install-rpm: rpm
	$(PKG_MGR) install -y .rpmbuild/RPMS/noarch/$(_MODULE)*

uninstall-rpm:
	$(PKG_MGR) remove -y $(_MODULE) || :

reinstall-rpm: uninstall-rpm install-rpm 

clean:
	$(RM) .rpmbuild
