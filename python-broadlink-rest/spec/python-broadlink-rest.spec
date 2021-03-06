%define _module python-broadlink-rest
%define project broadlink_rest

%{!?svn_revision:%define svn_revision 1}

# COMPATIBILITY FIX: Jenkins job name is neccessary to make build root unique (for CentOS5 and earlier)
%{!?JOB_NAME:%define JOB_NAME standalone}

%global debug_package %{nil}

Name:           python3-broadlink-rest
Version:        0.1
Release:        %{svn_revision}%{?dist}
Summary:        Python BroadLink RESTful server
Packager:       Roman Pavlyuk <roman.pavluyk@gmail.com>
Group:          Tools/Other
License:        Apache 2.0
URL:            https://github.com/rpavlyuk/python-broadlink-rest
Source0:        %{_module}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)-%{JOB_NAME}
BuildArch:      noarch


%if 0%{?rhel}
BuildRequires:  python36-setuptools
BuildRequires:  python3-rpm-macros

Requires:       python36
Requires:	python3-broadlink
Requires:       python36-pip
%endif

%if 0%{?fedora} >= 21
BuildRequires:  python3-setuptools
BuildRequires:  python3-rpm-macros

Requires:       python3
Requires:       python3-broadlink
Requires:       python3-pip
%endif



%description
Python BroadLink RESTful server that is based on python-broadlink library.

%prep
%setup -n %{_module}


%build
pushd ./src
%{py3_build}
popd

%install
pushd ./src 
%{py3_install}
popd

# Common files
mkdir -p "$RPM_BUILD_ROOT"
mkdir -p "$RPM_BUILD_ROOT"%{_datadir}/broadlink/rest
mkdir -p $RPM_BUILD_ROOT%{_unitdir}

cp -a src/broadlink_rest.ini "$RPM_BUILD_ROOT"%{_datadir}/broadlink/rest
cp -a extras/systemd/broadlink-server.service $RPM_BUILD_ROOT%{_unitdir}

%files
%{python3_sitelib}/*

%config(noreplace) %{_datadir}/broadlink/rest/broadlink_rest.ini

%{_unitdir}/broadlink-server.service

%doc src/README.md src/README.rst


%changelog
