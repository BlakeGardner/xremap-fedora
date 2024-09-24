Name:           xremap
Version:        0.10.1
Release:        1%{?dist}
Summary:        xremap is a key remapper for Linux. It supports app-specific remapping and Wayland.

License:        MIT
URL:            https://github.com/xremap/xremap
Source0:        https://github.com/xremap/xremap/archive/refs/tags/%{version}.tar.gz

BuildRequires:  rust
Requires:       gnome-shell

%description
xremap is a key remapper for Linux. It supports app-specific remapping and Wayland.

%prep
%autosetup


%build
%configure
%make_build


%install
%make_install


%files
%license add-license-file-here
%doc add-docs-here



%changelog
* Tue Sep 24 2024 Blake Gardner <blakerg@gmail.com>
- 
