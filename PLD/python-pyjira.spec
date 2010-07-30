# $Revision: 1.19 $, $Date: 2010/07/26 10:57:31 $
%define 	module	pyjira
%define		subver	20100730
Summary:	pyjira
Summary(pl.UTF-8):	pyjira
Name:		python-pyjira
Version:	0.0.0
Release:	0.%{subver}.1
License:	MIT
Group:		Development/Languages/Python
Source0:	pyjira.tar
URL:		http://github.com/pawelz/pyjira
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pyjira

%prep
%setup -q -n %{module}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%{py_sitescriptdir}/pyjira/*.py[co]
%{py_sitescriptdir}/pyjira-*.egg-info

%changelog
* Fri Jul 30 2010 Paweł Zuzelski <pawelz@pld-linux.org>

	- Initial version, based on PLD template-python.spec
