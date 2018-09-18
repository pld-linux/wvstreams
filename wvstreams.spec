#
# Conditional build:
%bcond_without	apidocs	# Doxygen documentation
%bcond_without	qt	# wvstreams-qt library

Summary:	A network programming library written in C++
Summary(pl.UTF-8):	Biblioteka programowania sieciowego napisana w C++
Name:		wvstreams
Version:	4.6.1
Release:	10
License:	LGPL v2
Group:		Libraries
#Source0Download: http://code.google.com/p/wvstreams/downloads/list
Source0:	http://wvstreams.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	2760dac31a43d452a19a3147bfde571c
Patch0:		%{name}-sort.patch
Patch1:		%{name}-tcl.patch
Patch2:		%{name}-qt.patch
Patch3:		%{name}-openssl.patch
Patch4:		%{name}-includes.patch
Patch5:		%{name}-4.2.2-multilib.patch
Patch6:		%{name}-4.5-noxplctarget.patch
Patch7:		%{name}-4.6.1-make.patch
Patch8:		%{name}-4.6.1-gcc47.patch
Patch9:		%{name}-4.6.1-magic.patch
Patch10:	gcc-6.patch
URL:		http://alumnit.ca/wiki/index.php?page=WvStreams
BuildRequires:	autoconf >= 2.50
BuildRequires:	boost-devel
BuildRequires:	dbus-devel >= 1.2.14
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel >= 0.9.7i
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
%{?with_qt:BuildRequires:	qt-devel >= 3}
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

%package qt
Summary:	WvStreams interface to Qt 3 library
Summary(pl.UTF-8):	Interfejs WvStreams do biblioteki Qt 3
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}

%description qt
WvStreams interface to Qt 3 library.

%description qt -l pl.UTF-8
Interfejs WvStreams do biblioteki Qt 3.

%package qt-devel
Summary:	WvStreams interface to Qt 3 library - development files
Summary(pl.UTF-8):	Interfejs WvStreams do biblioteki Qt 3 - pliki programistyczne
Group:		X11/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-qt = %{version}-%{release}
Requires:	qt-devel >= 3

%description qt-devel
WvStreams interface to Qt 3 library - development files.

%description qt-devel -l pl.UTF-8
Interfejs WvStreams do biblioteki Qt 3 - pliki programistyczne.

%package apidocs
Summary:	API documentation for WvStreams libraries
Summary(pl.UTF-8):	Dokumentacja API bibliotek WvStreams
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for WvStreams libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek WvStreams.

%package uniconfd
Summary:	Daemon for the UniConf configuration system
Summary(pl.UTF-8):	Demon dla systemu konfiguracji UniConf
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description uniconfd
UniConf is the One True Configuration system that includes all the
others because it has plugin backends and frontends. Or, less
grandiosely, it's a lightweight, distributed, cacheable tree of
strings.

uniconfd is necessary when you have more than one application, or
multiple instances of an application, sharing one configuration.
UniConf-enabled applications contact uniconfd which provides
notifications when any of their watched keys change.

%description uniconfd -l pl.UTF-8
UniConf to system Jedynie Słusznej Konfiguracji zawierający
wszystkie inne, ponieważ ma wtyczki backendowe i frontendowe.
Mniej górnolotnie mówiąc, jest to lekkie, rozproszone, cache'owalne
drzewo łańcuchów znaków.

uniconfd jest potrzebny w przypadku korzystania z jednej konfiguracji
przez więcej niż jedną aplikację lub wiele instancji aplikacji. Wtedy
aplikacje korzystające z UniConfa kontaktują się z uniconfd, który
zapewnia powiadomienia w przypadku zmiany dowolnego z obserwowanych
kluczy.

%package -n valgrind-wvstreams
Summary:	WvStreams support for Valgrind
Summary(pl.UTF-8):	Obsługa WvStreams dla Valgrinda
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	valgrind

%description -n valgrind-wvstreams
WvStreams support for Valgrind.

%description -n valgrind-wvstreams -l pl.UTF-8
Obsługa WvStreams dla Valgrinda.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%build
%{__autoconf}
# disable-optimization disables -O2 override
%configure \
	--disable-optimization \
	%{!?with_qt:--without-qt}

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
%attr(755,root,root) %{_bindir}/uni
%attr(755,root,root) %{_bindir}/wsd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/uniconf.conf
%attr(755,root,root) %{_libdir}/libuniconf.so.*.*
%attr(755,root,root) %{_libdir}/libwvbase.so.*.*
%attr(755,root,root) %{_libdir}/libwvdbus.so.*.*
%attr(755,root,root) %{_libdir}/libwvstreams.so.*.*
%attr(755,root,root) %{_libdir}/libwvutils.so.*.*
%{_mandir}/man8/uni.8*
%dir /var/lib/uniconf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wvtestrun
%attr(755,root,root) %{_libdir}/libuniconf.so
%attr(755,root,root) %{_libdir}/libwvbase.so
%attr(755,root,root) %{_libdir}/libwvdbus.so
%attr(755,root,root) %{_libdir}/libwvstreams.so
%attr(755,root,root) %{_libdir}/libwvutils.so
%{_libdir}/libwvtest.a
%{_includedir}/wvstreams
%exclude %{_includedir}/wvstreams/wvqthook.h
%exclude %{_includedir}/wvstreams/wvqtstreamclone.h
%{_pkgconfigdir}/libuniconf.pc
%{_pkgconfigdir}/libwvbase.pc
%{_pkgconfigdir}/libwvdbus.pc
%{_pkgconfigdir}/libwvstreams.pc
%{_pkgconfigdir}/libwvtest.pc
%{_pkgconfigdir}/libwvutils.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libwvstatic.a

%if %{with qt}
%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwvqt.so.*.*

%files qt-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwvqt.so
%{_includedir}/wvstreams/wvqthook.h
%{_includedir}/wvstreams/wvqtstreamclone.h
%{_pkgconfigdir}/libwvqt.pc
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc Docs/doxy-html/*
%endif

%files uniconfd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/uniconfd
%config(noreplace) %verify(not md5 mtime size) /var/lib/uniconf/uniconfd.ini
%{_mandir}/man8/uniconfd.8*

%files -n valgrind-wvstreams
%defattr(644,root,root,755)
%{_libdir}/valgrind/wvstreams.supp
