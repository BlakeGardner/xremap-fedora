Name:           xremap
Version:        0.10.1
Release:        1%{?dist}
Summary:        xremap is a key remapper for Linux. It supports app-specific remapping and Wayland.

License:        MIT
URL:            https://github.com/xremap/xremap
Source0:        https://github.com/xremap/xremap/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  rust, cargo
Requires:       gnome-shell

%description
xremap is a key remapper for Linux. It supports app-specific remapping and Wayland.

%prep
%autosetup -n %{name}-%{version}

%build
cargo build --release

%install
install -D -m 0755 target/release/xremap %{buildroot}%{_bindir}/xremap

%files
%license LICENSE
%doc README.md
%{_bindir}/xremap

%changelog
* Tue Sep 24 2024 Blake Gardner <blakerg@gmail.com> - 0.10.1-1
- Initial package
