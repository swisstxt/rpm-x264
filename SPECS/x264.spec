%global api 144

Name:           %{name}
Version:        %{ver}
Release:        %{rel}%{?dist}
Summary:        H264/AVC video streams encoder
BuildArch:      %{arch}
Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.videolan.org/developers/x264.html/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: perl-Digest-MD5-File
BuildRequires: zlib-devel openssl-devel libpng-devel libjpeg-devel
BuildRequires: yasm >= 1.0.0
Requires: %{name}-libs = %{version}-%{release}

Source: %{name}.tar.gz

%description
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

This package contains the frontend.

%package libs
Summary: Library for encoding H264/AVC video streams
Group: Development/Libraries

%description libs
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

%package devel
Summary: Development files for the x264 library
Group: Development/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

This package contains the development files.

%prep
%setup -q

%build
%configure \
	--prefix=%{_prefix} \
	--exec-prefix=%{_exec_prefix} \
	--bindir=%{_bindir} \
	--includedir=%{_includedir} \
	--extra-cflags="$RPM_OPT_FLAGS" \
	--enable-debug \
	--enable-shared \
	--system-libx264 \
	--enable-pic \
	--host=%{_target_platform} \
	--libdir=%{_libdir}

%{__make} %{?_smp_mflags}

%install
%{__make} DESTDIR=%{buildroot} install

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(644, root, root, 0755)
%doc AUTHORS COPYING
%attr(755,root,root) %{_bindir}/x264

%files libs
%defattr(644, root, root, 0755)
%{_libdir}/libx264.so.%{api}
#%{_libdir}/libx264.so

%files devel
%defattr(644, root, root, 0755)
%doc doc/*
%{_includedir}/x264.h
%{_includedir}/x264_config.h
%{_libdir}/libx264.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog