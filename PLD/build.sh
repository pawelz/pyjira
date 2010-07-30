#!/bin/sh -x

TOPDIR=$PWD
SPECDIR=$TOPDIR
SOURCEDIR=$TOPDIR
BUILDDIR=$TOPDIR/BUILD
RPMDIR=$(dirname $TOPDIR)
SRPMDIR=$(dirname $TOPDIR)

mkdir -p $BUILDDIR

(cd ..; git archive --prefix=pyjira/ HEAD --format=tar) > pyjira.tar

rpmbuild -bb \
	--define "_binary_payload w9.gzdio" \
	--define "_source_payload w9.gzdio" \
	--define "_topdir $TOPDIR" \
	--define "_sourcedir $SOURCEDIR" \
	--define "_specdir $SPECDIR" \
	--define "_rpmdir $RPMDIR" \
	--define "_srpmdir $SRPMDIR" \
	python-pyjira.spec $@ | sed "s/^\(Wrote: .*\.rpm\)\$/$(tput setaf 1; tput bold)\1$(tput sgr0)/"
