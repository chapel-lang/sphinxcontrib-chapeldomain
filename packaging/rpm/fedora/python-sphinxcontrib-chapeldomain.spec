Name:           python-sphinxcontrib-chapeldomain
Version:        0.0.39
Release:        %autorelease
Summary:        Chapel domain for Sphinx

# The entire source is Apache-2.0, except that
# sphinxcontrib/chapeldomain/README.md is BSD-2-Clause
# (sphinxcontrib/chapeldomain/LICENSE).
License:        Apache-2.0 AND BSD-2-Clause
URL:            https://github.com/chapel-lang/sphinxcontrib-chapeldomain
# PyPI source does not have documentation
Source:         %{url}/archive/%{version}/sphinxcontrib-chapeldomain-%{version}.tar.gz
# Relax pinned dependency requirements
Patch:          relax-dep-requirements.patch

BuildArch:      noarch
BuildRequires:  python3-devel
# Documentation requirements
BuildRequires:  make
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-rtd-theme)
BuildRequires:  python3dist(snowballstemmer)
BuildRequires:  texinfo
# Test requirements
BuildRequires:  python3dist(pytest)
# chapel.py is vendored from Pygments; see
# sphinxcontrib/chapeldomain/README.md for justification
Provides:       bundled(python3dist(pygments))

%global _description %{expand:
Chapel domain for Sphinx.}

%description %_description

%package -n     python3-sphinxcontrib-chapeldomain
Summary:        %{summary}

%description -n python3-sphinxcontrib-chapeldomain %_description


%prep
%autosetup -p1 -n sphinxcontrib-chapeldomain-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel
pushd docs
make texinfo
pushd _build
pushd texinfo
makeinfo --docbook ChapelDomain.texi
popd
popd
popd

%install
%pyproject_install
%pyproject_save_files -l sphinxcontrib
mkdir -p %{buildroot}%{_datadir}/help/en/python-sphinxcontrib-chapeldomain
install -p -m644 docs/_build/texinfo/ChapelDomain.xml \
   %{buildroot}%{_datadir}/help/en/python-sphinxcontrib-chapeldomain

%check
%pyproject_check_import
%pytest

%files -n python3-sphinxcontrib-chapeldomain -f %{pyproject_files}
%{python3_sitelib}/sphinxcontrib_chapeldomain-%{version}-py%{python3_version}-nspkg.pth
%doc README.rst
%doc %dir  %{_datadir}/help/en
%doc %lang(en) %{_datadir}/help/en/python-sphinxcontrib-chapeldomain

%changelog
%autochangelog
