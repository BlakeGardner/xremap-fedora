Name:           xremap
Version:        0.10.1
Release:        1%{?dist}
Summary:        A key remapper for Linux supporting app-specific remapping and Wayland.

License:        MIT
URL:            https://github.com/xremap/xremap
Source0:        https://github.com/xremap/xremap/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  rust, cargo

%description
xremap is a key remapper for Linux. It supports app-specific remapping and Wayland.

### Subpackage: GNOME
%package gnome
Summary:        xremap with GNOME Wayland support
Conflicts:      %{name}, %{name}-x11, %{name}-kde, %{name}-wlroots
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} < %{version}-%{release}
Requires:       gnome-shell

%description gnome
This variant of xremap is built with GNOME Wayland support.

### Subpackage: X11
%package x11
Summary:        xremap with X11 support
Conflicts:      %{name}, %{name}-gnome, %{name}-kde, %{name}-wlroots
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} < %{version}-%{release}
Requires:       xorg-x11-server-Xorg

%description x11
This variant of xremap is built with X11 support.

### Subpackage: KDE
%package kde
Summary:        xremap with KDE-Plasma Wayland support
Conflicts:      %{name}, %{name}-gnome, %{name}-x11, %{name}-wlroots
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} < %{version}-%{release}
Requires:       plasma-workspace

%description kde
This variant of xremap is built with KDE-Plasma Wayland support.

### Subpackage: wlroots
%package wlroots
Summary:        xremap with wlroots support (Sway, Hyprland, etc.)
Conflicts:      %{name}, %{name}-gnome, %{name}-x11, %{name}-kde
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} < %{version}-%{release}

%description wlroots
This variant of xremap is built with wlroots support for Sway, Hyprland, etc.

%prep
%autosetup -n %{name}-%{version}

%build
### Build the base package without any features
cargo build --release

### Build each variant in separate target directories to avoid conflicts
### GNOME build
cargo build --release --features gnome --target-dir target-gnome

### X11 build
cargo build --release --features x11 --target-dir target-x11

### KDE build
cargo build --release --features kde --target-dir target-kde

### wlroots build
cargo build --release --features wlroots --target-dir target-wlroots

%install
### Install the base package binary
install -D -m 0755 target/release/xremap %{buildroot}%{_bindir}/xremap

### Install variant binaries to temporary locations
install -D -m 0755 target-gnome/release/xremap %{buildroot}%{_libexecdir}/xremap/xremap-gnome
install -D -m 0755 target-x11/release/xremap %{buildroot}%{_libexecdir}/xremap/xremap-x11
install -D -m 0755 target-kde/release/xremap %{buildroot}%{_libexecdir}/xremap/xremap-kde
install -D -m 0755 target-wlroots/release/xremap %{buildroot}%{_libexecdir}/xremap/xremap-wlroots

%files
%license LICENSE
%doc README.md
%{_bindir}/xremap

%files gnome
%license LICENSE
%doc README.md
%{_bindir}/xremap

%post gnome
cp -f %{_libexecdir}/xremap/xremap-gnome %{_bindir}/xremap

%files x11
%license LICENSE
%doc README.md
%{_bindir}/xremap

%post x11
cp -f %{_libexecdir}/xremap/xremap-x11 %{_bindir}/xremap

%files kde
%license LICENSE
%doc README.md
%{_bindir}/xremap

%post kde
cp -f %{_libexecdir}/xremap/xremap-kde %{_bindir}/xremap

%files wlroots
%license LICENSE
%doc README.md
%{_bindir}/xremap

%post wlroots
cp -f %{_libexecdir}/xremap/xremap-wlroots %{_bindir}/xremap

%changelog
* Tue Sep 24 2024 Blake Gardner <blakerg@gmail.com> - 0.10.1-1
- Initial package with base and subpackages for GNOME, X11, KDE, and wlroots.
