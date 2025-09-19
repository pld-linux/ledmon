#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	Enclosure LED Utilities
Name:		ledmon
Version:	1.1.0
Release:	2
License:	GPL v2.0 AND LGPL v2.1
Group:		Libraries
Source0:	https://github.com/intel/ledmon/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5cd888ac13b9afe1dae11d421bd8e17d
URL:		https://github.com/intel/ledmon
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 2.011
Requires(post,preun,postun):	systemd-units >= 1:250.1
Requires:	libled = %{version}-%{release}
Requires:	systemd-units >= 1:250.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ledmon and ledctl are user space applications design to control
LED associated with each slot in an enclosure or a drive bay. There
are two types of system: 2-LED system (Activity LED, Status LED) and
3-LED system (Activity LED, Locate LED, Fail LED). User must have root
privileges to use this application.

%package -n libled
Summary:	Common files for libled library
Summary(pl.UTF-8):	Wspólne pliki biblioteki libled
Group:		Libraries

%description -n libled
Common files for libled library.

%description -n libled -l pl.UTF-8
Wspólne pliki biblioteki libled.

%package -n libled-devel
Summary:	Header files for libled library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libled
Group:		Development/Libraries
Requires:	libled = %{version}-%{release}

%description -n libled-devel
Header files for libled library.

%description -n libled-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libled.

%package -n libled-static
Summary:	Static libled library
Summary(pl.UTF-8):	Statyczna biblioteka libled
Group:		Development/Libraries
Requires:	libled-devel = %{version}-%{release}

%description -n libled-static
Static libled library.

%description -n libled-static -l pl.UTF-8
Statyczna biblioteka libled.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-systemd \
	--enable-library \
	%{!?with_static_libs:--disable-static}
%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post ledmon.service

%preun
%systemd_preun ledmon.service

%postun
%systemd_postun_with_restart ledmon.service

%post -n libled -p /sbin/ldconfig
%postun -n libled -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_sbindir}/ledctl
%attr(755,root,root) %{_sbindir}/ledmon
%{_mandir}/man5/ledmon.conf.5*
%{_mandir}/man8/ledctl.8*
%{_mandir}/man8/ledmon.8*
%{systemdunitdir}/ledmon.service

%files -n libled
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libled.so.*.*.*
%ghost %{_libdir}/libled.so.1

%files -n libled-devel
%defattr(644,root,root,755)
%doc CHANGELOG.md
%{_libdir}/libled.so
%{_includedir}/led
%{_pkgconfigdir}/ledmon.pc

%if %{with static_libs}
%files -n libled-static
%defattr(644,root,root,755)
%{_libdir}/libled.a
%endif
