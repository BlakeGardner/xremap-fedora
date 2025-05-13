Name:           xremap
Version:        0.10.12
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
install -D -m 0755 target-vanilla/release/xremap %{buildroot}%{_bindir}/xremap-vanilla

# Install GNOME variant
install -D -m 0755 target-gnome/release/xremap %{buildroot}%{_bindir}/xremap-gnome

# Install X11 variant
install -D -m 0755 target-x11/release/xremap %{buildroot}%{_bindir}/xremap-x11

# Install KDE variant
install -D -m 0755 target-kde/release/xremap %{buildroot}%{_bindir}/xremap-kde

# Install wlroots variant
install -D -m 0755 target-wlroots/release/xremap %{buildroot}%{_bindir}/xremap-wlroots

# Install udev rules
install -D -m 0644 %{SOURCE1} %{buildroot}/usr/lib/udev/rules.d/00-xremap-input.rules

%pre
# Create 'input' group if it doesn't exist
getent group input >/dev/null || groupadd -r input

%post
# Vanilla variant
alternatives --install %{_bindir}/xremap xremap %{_bindir}/xremap-vanilla 10

%preun
if [ $1 -eq 0 ]; then
    alternatives --remove xremap %{_bindir}/xremap-vanilla
fi

%post gnome
alternatives --install %{_bindir}/xremap xremap %{_bindir}/xremap-gnome 20

%preun gnome
if [ $1 -eq 0 ]; then
    alternatives --remove xremap %{_bindir}/xremap-gnome
fi

%post x11
alternatives --install %{_bindir}/xremap xremap %{_bindir}/xremap-x11 20

%preun x11
if [ $1 -eq 0 ]; then
    alternatives --remove xremap %{_bindir}/xremap-x11
fi

%post kde
alternatives --install %{_bindir}/xremap xremap %{_bindir}/xremap-kde 20

%preun kde
if [ $1 -eq 0 ]; then
    alternatives --remove xremap %{_bindir}/xremap-kde
fi

%post wlroots
alternatives --install %{_bindir}/xremap xremap %{_bindir}/xremap-wlroots 20

%preun wlroots
if [ $1 -eq 0 ]; then
    alternatives --remove xremap %{_bindir}/xremap-wlroots
fi

%files
%license LICENSE
%doc README.md
%{_bindir}/xremap-vanilla
/usr/lib/udev/rules.d/00-xremap-input.rules

%files gnome
%license LICENSE
%doc README.md
%{_bindir}/xremap-gnome
/usr/lib/udev/rules.d/00-xremap-input.rules

%files x11
%license LICENSE
%doc README.md
%{_bindir}/xremap-x11
/usr/lib/udev/rules.d/00-xremap-input.rules

%files kde
%license LICENSE
%doc README.md
%{_bindir}/xremap-kde
/usr/lib/udev/rules.d/00-xremap-input.rules

%files wlroots
%license LICENSE
%doc README.md
%{_bindir}/xremap-wlroots
/usr/lib/udev/rules.d/00-xremap-input.rules

%changelog
* Tue May 13 2025 Blake Gardner <blakerg@gmail.com> - 0.10.12-1
- Update xremap to upstream version 0.10.12

* Sun Apr 27 2025 Blake Gardner <blakerg@gmail.com> - 0.10.11-1
- Update xremap to upstream version 0.10.11

* Sat Apr 19 2025 Blake Gardner <blakerg@gmail.com> - 0.10.10-1
- Update xremap to upstream version 0.10.10

* Mon Feb 17 2025 Blake Gardner <blakerg@gmail.com> - 0.10.8-1
- Update xremap to upstream version 0.10.8

* Mon Feb 17 2025 Blake Gardner <blakerg@gmail.com> - 0.10.5-1
- Update xremap to upstream version 0.10.5

* Sun Dec 29 2024 Blake Gardner <blakerg@gmail.com> - 0.10.3-1
- Update xremap to upstream version 0.10.3

* Wed Oct 23 2024 Blake Gardner <blakerg@gmail.com> - 0.10.2-1
- Update xremap to upstream version 0.10.2

* Tue Sep 27 2024 Blake Gardner <blakerg@gmail.com> - 0.10.1-5
- Fix RPM macros

* Tue Sep 27 2024 Blake Gardner <blakerg@gmail.com> - 0.10.1-4
- Use alternatives system to manage multiple xremap binaries

* Tue Sep 27 2024 Blake Gardner <blakerg@gmail.com> - 0.10.1-3
- Re-enabled debug rpms and debug symbols in Rust binaries

* Tue Sep 25 2024 Blake Gardner <blakerg@gmail.com> - 0.10.1-2
- Disabled debug info RPM builds and removed debug symbols from Rust binaries

* Tue Sep 24 2024 Blake Gardner <blakerg@gmail.com> - 0.10.1-1
- Initial package release
