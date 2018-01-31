%define		mod_name	log_gelf
%define 	apxs		%{_sbindir}/apxs
Summary:	Apache2 module for writing access logs to Graylog
Name:		apache-mod_%{mod_name}
Version:	0.2.0
Release:	1
License:	Apache v2.0
Group:		Networking/Daemons/HTTP
Source0:	https://github.com/graylog-labs/apache-mod_log_gelf/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4aba4fd0f8e1175c39d4ac236282df10
Source1:	apache.conf
Patch0:		build.patch
URL:		https://github.com/graylog-labs/apache-mod_log_gelf
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.2
BuildRequires:	json-c-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
Apache2 module for writing access logs to Graylog.

%prep
%setup -q -n apache-mod_log_gelf-%{version}
%patch0 -p1

%build
%{__make} -C src

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}
%{__make} -C src install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README.md
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/mod_%{mod_name}.so
