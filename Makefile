HOME=$(shell pwd)
VERSION="1"
RELEASE=$(shell /opt/buildhelper/buildhelper getgitrev .)
NAME=x264
SPEC=$(shell /opt/buildhelper/buildhelper getspec ${NAME})
ARCH=$(shell /opt/buildhelper/buildhelper getarch)
OS_RELEASE=$(shell /opt/buildhelper/buildhelper getosrelease)

all: build

clean:
	rm -rf ./rpmbuild
	rm -rf ./SOURCES
	mkdir -p ./rpmbuild/SPECS/ ./rpmbuild/SOURCES/
	mkdir -p ./SPECS ./SOURCES

getsources:
	git clone --depth 1 git://git.videolan.org/x264 ./SOURCES/${NAME}-${VERSION}
	( cd ./SOURCES && tar -czvf ${NAME}.tar.gz ${NAME}-${VERSION}/ )
	rm -rf ./SOURCES/x264/

build: clean getsources
	cp -r ./SPECS/* ./rpmbuild/SPECS/ || true
	cp -r ./SOURCES/* ./rpmbuild/SOURCES/ || true
	rpmbuild -ba ${SPEC} \
	--define "ver ${VERSION}" \
	--define "rel ${RELEASE}" \
	--define "name ${NAME}" \
	--define "os_rel ${OS_RELEASE}" \
	--define "arch ${ARCH}" \
	--define "_topdir %(pwd)/rpmbuild" \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \

publish:
	echo "/opt/buildhelper/buildhelper pushrpm yum-01.stxt.media.int:8080/swisstxt-centos"