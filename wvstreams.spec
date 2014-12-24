#
# TODO:
#   - check and/or package files:
#    /etc/uniconf.conf
#    /usr/bin/uni
#    /usr/bin/wsd
#    /usr/bin/wvtestrunner.pl
#    /usr/lib/valgrind/wvstreams.supp
#    /usr/sbin/uniconfd
#    /usr/share/man/man8/uni.8.gz
#    /usr/share/man/man8/uniconfd.8.gz
#    /var/lib/uniconf/uniconfd.ini
#
#
# Conditional build:
%bcond_without	apidocs	# Doxygen documentation
%bcond_without	slp	# OpenSLP support
#
Summary:	A network programming library written in C++
Summary(pl.UTF-8):	Biblioteka programowania sieciowego napisana w C++
Name:		wvstreams
Version:	4.6.1
Release:	5
License:	LGPL
Group:		Libraries
#Source0Download: http://code.google.com/p/wvstreams/downloads/list
Source0:	http://wvstreams.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	2760dac31a43d452a19a3147bfde571c
Patch0:		%{name}-sort.patch
Patch3:		%{name}-openssl.patch
Patch4:		%{name}-includes.patch
Patch5:		%{name}-4.2.2-multilib.patch
Patch6:		%{name}-4.5-noxplctarget.patch
Patch7:		%{name}-4.6.1-make.patch
Patch8:		%{name}-4.6.1-gcc47.patch
Patch9:		%{name}-4.6.1-magic.patch
URL:		http://alumnit.ca/wiki/index.php?page=WvStreams
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	boost-devel
BuildRequires:	dbus-devel >= 1.2.14
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel
%{?with_slp:BuildRequires:	openslp-devel}
BuildRequires:	openssl-devel >= 0.9.7i
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	tcl-devel
BuildRequires:	zlib-devel
Obsoletes:	libwvstreams
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development.

%description -l pl.UTF-8
WvStreams próbuje być wydajną, bezpieczną i łatwą w użyciu biblioteką
do tworzenia aplikacji sieciowych.

%package devel
Summary:	Development files for WvStreams
Summary(pl.UTF-8):	Pliki developerskie dla WvStreams
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Obsoletes:	libwvstreams-devel

%description devel
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development. This package contains the
files needed for developing applications which use WvStreams.

%description devel -l pl.UTF-8
WvStreams próbuje być wydajną, bezpieczną i łatwą w użyciu biblioteką
do tworzenia aplikacji sieciowych. Pakiet ten zawiera pliki niezbędne
do kompilowania oprogramowania używającego WvStreams.

%package static
Summary:	Static WvStreams library
Summary(pl.UTF-8):	Statyczna biblioteka WvStreams
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static WvStreams library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki WvStreams.

%package apidocs
Summary:	API documentation for WvStreams libraries
Summary(pl.UTF-8):	Dokumentacja API bibliotek WvStreams
Group:		Documentation

%description apidocs
API documentation for WvStreams libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek WvStreams.

%prep
%setup -q
%patch0 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
# disable-optimization disables -O2 override
%configure \
	--disable-optimization \
	--with-openslp%{!?with_slp:=no} \
	--without-vorbis

%{__make} -j1 \
	VPATH=%{_libdir} \
	DEBUG=%{?debug:1}%{!?debug:0} \
	CXX="%{__cxx}" \
	VERBOSE=1 \
	CXXOPTS="%{rpmcxxflags} -fPIC -fpermissive -fno-strict-aliasing -fno-tree-dce -fno-optimize-sibling-calls"
	COPTS="%{rpmcflags} -fPIC -fPIC -fno-strict-aliasing"

%if %{with apidocs}
%{__make} doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_libdir}/libuniconf.so.*.*
%attr(755,root,root) %{_libdir}/libwvbase.so.*.*
%attr(755,root,root) %{_libdir}/libwvdbus.so.*.*
%attr(755,root,root) %{_libdir}/libwvstreams.so.*.*
%attr(755,root,root) %{_libdir}/libwvutils.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libuniconf.so
%attr(755,root,root) %{_libdir}/libwvbase.so
%attr(755,root,root) %{_libdir}/libwvdbus.so
%attr(755,root,root) %{_libdir}/libwvstreams.so
%attr(755,root,root) %{_libdir}/libwvutils.so
%{_libdir}/libwvtest.a
%{_includedir}/wvstreams
%{_pkgconfigdir}/libuniconf.pc
%{_pkgconfigdir}/libwvbase.pc
%{_pkgconfigdir}/libwvdbus.pc
#%{_pkgconfigdir}/libwvqt.pc
%{_pkgconfigdir}/libwvstreams.pc
%{_pkgconfigdir}/libwvtest.pc
%{_pkgconfigdir}/libwvutils.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libwvstatic.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc Docs/doxy-html/*
%endif
