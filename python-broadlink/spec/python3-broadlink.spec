%define _module python-broadlink
%define project broadlink

%{!?svn_revision:%define svn_revision 1}

# COMPATIBILITY FIX: Jenkins job name is neccessary to make build root unique (for CentOS5 and earlier)
%{!?JOB_NAME:%define JOB_NAME standalone}

%global debug_package %{nil}

Name:           python3-%{project}
Version:        0.5
Release:        %{svn_revision}%{?dist}
Summary:        Python BroadLink library to control BroadLink smart home devices (forked by eschava)
Packager:       Roman Pavlyuk <roman.pavluyk@gmail.com>
Group:          Tools/Other
License:        GPLv3
URL:            https://github.com/eschava/python-broadlink
Source0:        %{_module}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)-%{JOB_NAME}
BuildArch:      noarch

BuildRequires:  python-setuptools
BuildRequires:  python-rpm-macros
BuildRequires:  python3-rpm-macros

%if 0%{?fedora}
Requires:       python3
Requires:       python3-pyaes

BuildRequires:  python-setuptools
%endif

%if 0%{?rhel}
Requires:       python34
Requires:       python34-crypto

BuildRequires:	python34-setuptools
%endif


%description
Python BroadLink library to control BroadLink smart home devices. 

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

mkdir -p "$RPM_BUILD_ROOT"%{_bindir}
cp -a src/cli/broadlink_* "$RPM_BUILD_ROOT"%{_bindir}

%files
%{python3_sitelib}/*

%attr(0755, root, root) %{_bindir}/*

%doc src/README.md src/protocol.md src/cli/README.md


%changelog
