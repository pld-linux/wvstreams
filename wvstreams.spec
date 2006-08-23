#
# TODO:
#   - check and/or package files:
#
#   /etc/uniconf.conf
#   /usr/bin/uni
#   /usr/lib64/pkgconfig/liboggspeex.pc
#   /usr/lib64/pkgconfig/liboggvorbis.pc
#   /usr/lib64/pkgconfig/libuniconf.pc
#   /usr/lib64/pkgconfig/libwvbase.pc
#   /usr/lib64/pkgconfig/libwvfft.pc
#   /usr/lib64/pkgconfig/libwvqt.pc
#   /usr/lib64/pkgconfig/libwvstreams.pc
#   /usr/lib64/pkgconfig/libwvutils.pc
#   /usr/lib64/pkgconfig/wvxplc.pc
#   /usr/sbin/uniconfd
#   /usr/share/man/man8/uni.8.gz
#   /usr/share/man/man8/uniconfd.8.gz
#   /var/lib/uniconf/uniconfd.ini
#
# Conditional build:
%bcond_without	doc	# don't build documentation
#
Summary:	A network programming library written in C++
Summary(pl):	Biblioteka programowania sieciowego napisana w C++
Name:		wvstreams
Version:	4.0.2
Release:	2
License:	LGPL
Group:		Libraries
Source0:	http://www.csclub.uwaterloo.ca/~ja2morri/%{name}-%{version}.tar.gz
# Source0-md5:	ecb4e74ebaa1f45206f5d88eb34c5623
Patch0:		%{name}-cflags.patch
Patch1:		%{name}-gcc4.patch
Patch2:		%{name}-unresolved_symbols.patch
Patch3:		%{name}-mk.patch
URL:		http://open.nit.ca/wvstreams/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_doc:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel >= 0.9.7i
Obsoletes:	libwvstreams
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development.

%description -l pl
WvStreams próbuje byæ wydajn±, bezpieczn± i ³atw± w u¿yciu bibliotek±
do tworzenia aplikacji sieciowych.

%package devel
Summary:	Development files for WvStreams
Summary(pl):	Pliki developerskie dla WvStreams
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Obsoletes:	libwvstreams-devel

%description devel
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development. This package contains the
files needed for developing applications which use WvStreams.

%description devel -l pl
WvStreams próbuje byæ wydajn±, bezpieczn± i ³atw± w u¿yciu bibliotek±
do tworzenia aplikacji sieciowych. Pakiet ten zawiera pliki niezbêdne
do tworzenia aplikacji u¿ywaj±cych WvStreams.

%package static
Summary:	Static wvstreams library
Summary(pl):	Statyczna biblioteka wvstreams
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static wvstreams library.

%description static -l pl
Statyczna wersja biblioteki wvstreams.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
#ugly hack - fix it
cp include/wvsslhacks.h crypto
cp include/wvtelephony.h telephony

%build
cd xplc
cp -f /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure
cd ..

# despite .fpic rules the same .o files are used for .a and .so - need -fPIC
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	--without-vorbis

%{__make} -j1 \
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
%if %{with doc}
%doc Docs/doxy-html/*
%endif
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/wvstreams

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
