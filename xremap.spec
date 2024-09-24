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

### Subpackage descriptions
%package gnome
Summary:        xremap with GNOME Wayland support
Conflicts:      %{name}-x11 %{name}-kde %{name}-wlroots
Requires:       %{name} = %{version}-%{release}
Requires:       gnome-shell

%description gnome
This variant of xremap is built with GNOME Wayland support.

%package x11
Summary:        xremap with X11 support
Conflicts:      %{name}-gnome %{name}-kde %{name}-wlroots
Requires:       %{name} = %{version}-%{release}
Requires:       xorg-x11-server-Xorg

%description x11
This variant of xremap is built with X11 support.

%package kde
Summary:        xremap with KDE-Plasma Wayland support
Conflicts:      %{name}-gnome %{name}-x11 %{name}-wlroots
Requires:       %{name} = %{version}-%{release}
Requires:       plasma-workspace

%description kde
This variant of xremap is built with KDE-Plasma Wayland support.

%package wlroots
Summary:        xremap with wlroots support for Sway, Hyprland, etc.
Conflicts:      %{name}-gnome %{name}-x11 %{name}-kde
Requires:       %{name} = %{version}-%{release}

%description wlroots
This variant of xremap is built with wlroots support (for Sway, Hyprland, etc.).


%prep
%autosetup -n %{name}-%{version}

%build
### Build for each feature
mkdir -p build/{gnome,x11,kde,wlroots}

### GNOME build
pushd build/gnome
cargo build --release --features gnome
popd

### X11 build
pushd build/x11
cargo build --release --features x11
popd

### KDE build
pushd build/kde
cargo build --release --features kde
popd

### wlroots build
pushd build/wlroots
cargo build --release --features wlroots
popd


%install
### Install the binary from the correct build path
install -D -m 0755 %{_builddir}/xremap-%{version}/target/release/xremap %{buildroot}%{_bindir}/xremap


%files
%license LICENSE
%doc README.md
%{_bindir}/xremap

%files gnome
%{_bindir}/xremap

%files x11
%{_bindir}/xremap

%files kde
%{_bindir}/xremap

%files wlroots
%{_bindir}/xremap


%changelog
* Tue Sep 24 2024 Blake Gardner <blakerg@gmail.com> - 0.10.1-1
- Initial package with subpackages for GNOME, X11, KDE, and wlroots.
