Name:           xremap
Version:        0.10.1
Release:        1%{?dist}
%define _debugsource_template %{nil}
Summary:        A key remapper for Linux supporting app-specific remapping and Wayland.

License:        MIT
URL:            https://github.com/xremap/xremap
Source0:        https://github.com/xremap/xremap/archive/refs/tags/v%{version}.tar.gz
Source1:        00-xremap-input.rules

BuildRequires:  rust, cargo

%description
xremap is a key remapper for Linux. It supports app-specific remapping and Wayland.

### **Main Package**
Conflicts:      %{name}-gnome, %{name}-x11, %{name}-kde, %{name}-wlroots
Obsoletes:      %{name} < %{version}-%{release}

%package gnome
Summary:        xremap with GNOME Wayland support
Conflicts:      %{name}, %{name}-x11, %{name}-kde, %{name}-wlroots
Requires:       gnome-shell

%description gnome
This variant of xremap is built with GNOME Wayland support.

%package x11
Summary:        xremap with X11 support
Conflicts:      %{name}, %{name}-gnome, %{name}-kde, %{name}-wlroots
Requires:       xorg-x11-server-Xorg

%description x11
This variant of xremap is built with X11 support.

%package kde
Summary:        xremap with KDE Plasma Wayland support
Conflicts:      %{name}, %{name}-gnome, %{name}-x11, %{name}-wlroots
Requires:       plasma-workspace

%description kde
This variant of xremap is built with KDE Plasma Wayland support.

%package wlroots
Summary:        xremap with wlroots support (Sway, Hyprland, etc.)
Conflicts:      %{name}, %{name}-gnome, %{name}-x11, %{name}-kde

%description wlroots
This variant of xremap is built with wlroots support for compositors like Sway and Hyprland.

%prep
%autosetup -n %{name}-%{version}

%build
# Build vanilla variant
export RUSTFLAGS="-C debuginfo=2 -C metadata=vanilla"
cargo build --release --target-dir target-vanilla

# Build GNOME variant
export RUSTFLAGS="-C debuginfo=2 -C metadata=gnome"
cargo build --release --features gnome --target-dir target-gnome

# Build X11 variant
export RUSTFLAGS="-C debuginfo=2 -C metadata=x11"
cargo build --release --features x11 --target-dir target-x11

# Build KDE variant
export RUSTFLAGS="-C debuginfo=2 -C metadata=kde"
cargo build --release --features kde --target-dir target-kde

# Build wlroots variant
export RUSTFLAGS="-C debuginfo=2 -C metadata=wlroots"
cargo build --release --features wlroots --target-dir target-wlroots

%install
rm -rf %{buildroot}

# Install vanilla variant
install -D -m 0755 target-vanilla/release/xremap %{buildroot}%{_bindir}/xremap

# Install GNOME variant
install -D -m 0755 target-gnome/release/xremap %{buildroot}%{_bindir}/xremap

# Install X11 variant
install -D -m 0755 target-x11/release/xremap %{buildroot}%{_bindir}/xremap

# Install KDE variant
install -D -m 0755 target-kde/release/xremap %{buildroot}%{_bindir}/xremap

# Install wlroots variant
install -D -m 0755 target-wlroots/release/xremap %{buildroot}%{_bindir}/xremap

# Install udev rules
install -D -m 0644 %{SOURCE1} %{buildroot}/usr/lib/udev/rules.d/00-xremap-input.rules

%pre
# Create 'input' group if it doesn't exist
getent group input >/dev/null || groupadd -r input

%post
# Reload udev rules
udevadm control --reload-rules
udevadm trigger

%files
%license LICENSE
%doc README.md
%{_bindir}/xremap
/usr/lib/udev/rules.d/00-xremap-input.rules

%files gnome
%license LICENSE
%doc README.md
%{_bindir}/xremap
/usr/lib/udev/rules.d/00-xremap-input.rules

%files x11
%license LICENSE
%doc README.md
%{_bindir}/xremap
/usr/lib/udev/rules.d/00-xremap-input.rules

%files kde
%license LICENSE
%doc README.md
%{_bindir}/xremap
/usr/lib/udev/rules.d/00-xremap-input.rules

%files wlroots
%license LICENSE
%doc README.md
%{_bindir}/xremap
/usr/lib/udev/rules.d/00-xremap-input.rules

%changelog
* Tue Sep 24 2024 Blake Gardner <blakerg@gmail.com> - 0.10.1-1
- Initial package release
