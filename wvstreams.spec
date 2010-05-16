#
# TODO:
#   - review patches: vstreams-cflags.patch, wvstreams-mk.patch
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
%bcond_without	doc	# don't build documentation
%bcond_without	slp	# build without openslp
#
Summary:	A network programming library written in C++
Summary(pl.UTF-8):	Biblioteka programowania sieciowego napisana w C++
Name:		wvstreams
Version:	4.6.1
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://wvstreams.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	2760dac31a43d452a19a3147bfde571c
Patch0:		%{name}-sort.patch
Patch1:		%{name}-cflags.patch
Patch2:		%{name}-mk.patch
Patch3:		%{name}-openssl.patch
URL:		http://alumnit.ca/wiki/index.php?page=WvStreams
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	boost-devel
BuildRequires:	dbus-devel >= 1.2.14
%{?with_doc:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel
%{?with_slp:BuildRequires:	openslp-devel}
BuildRequires:	openssl-devel >= 0.9.7i
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	tcl-devel
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
do tworzenia aplikacji używających WvStreams.

%package static
Summary:	Static wvstreams library
Summary(pl.UTF-8):	Statyczna biblioteka wvstreams
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static wvstreams library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki wvstreams.

%prep
%setup -q
%patch0 -p1
%patch3 -p1

%build
%configure \
	--with%{!?with_slp:out}-openslp \
	--without-vorbis

%{__make} -j1 \
	VPATH=%{_libdir} \
	DEBUG=%{?debug:1}%{!?debug:0} \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC -DDEBUG=0 \$(OSDEFINE)"

%if %{with doc}
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
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
#%if %{with doc}
#%doc Docs/doxy-html/*
#%endif
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/wvstreams
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
