Summary:	A network programming library written in C++
Summary(pl):	Biblioteka programowania sieciowego napisana w C++
Name:		wvstreams
Version:	3.70
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://open.nit.ca/download/%{name}-%{version}.tar.gz
BuildRequires:	openssl-devel >= 0.9.7
URL:		http://open.nit.ca/wvstreams/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	libwvstreams

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
Requires:	%{name} = %{version}
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
Requires:	%{name}-devel = %{version}

%description static
Static wvstreams library.

%description static -l pl
Statyczna wersja biblioteki wvstreams.

%prep
%setup  -q

%build
%{__make} CXX="%{__cxx}"
%{__make} doxygen

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc src/README
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc dox/html/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/wvstreams

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
