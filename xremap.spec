Name:           xremap
Version:        0.14.6
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
Conflicts:      %{name}-gnome, %{name}-x11, %{name}-kde, %{name}-wlroots, %{name}-hypr, %{name}-niri

%package gnome
Summary:        xremap with GNOME Wayland support
Conflicts:      %{name}, %{name}-x11, %{name}-kde, %{name}-wlroots, %{name}-hypr, %{name}-niri
Requires:       gnome-shell

%description gnome
This variant of xremap is built with GNOME Wayland support.

%package x11
Summary:        xremap with X11 support
Conflicts:      %{name}, %{name}-gnome, %{name}-kde, %{name}-wlroots, %{name}-hypr, %{name}-niri
Requires:       xorg-x11-server-Xorg

%description x11
This variant of xremap is built with X11 support.

%package kde
Summary:        xremap with KDE Plasma Wayland support
Conflicts:      %{name}, %{name}-gnome, %{name}-x11, %{name}-wlroots, %{name}-hypr, %{name}-niri
Requires:       plasma-workspace

%description kde
This variant of xremap is built with KDE Plasma Wayland support.

%package wlroots
Summary:        xremap with wlroots support (Sway, etc.)
Conflicts:      %{name}, %{name}-gnome, %{name}-x11, %{name}-kde, %{name}-hypr, %{name}-niri

%description wlroots
This variant of xremap is built with wlroots support for compositors like Sway.

%package hypr
Summary:        xremap with Hyprland support
Conflicts:      %{name}, %{name}-gnome, %{name}-x11, %{name}-kde, %{name}-wlroots, %{name}-niri
Requires: hyprland

%description hypr
This variant of xremap is built with Hyprland support.

%package niri
Summary:        xremap with Niri support
Conflicts:      %{name}, %{name}-gnome, %{name}-x11, %{name}-kde, %{name}-wlroots, %{name}-hypr
Requires: niri

%description niri
This variant of xremap is built with Niri support.

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

# Build hypr variant
export RUSTFLAGS="-C debuginfo=2 -C metadata=hypr"
cargo build --release --features hypr --target-dir target-hypr

# Build niri variant
export RUSTFLAGS="-C debuginfo=2 -C metadata=niri"
cargo build --release --features niri --target-dir target-niri

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

# Install hypr variant
install -D -m 0755 target-hypr/release/xremap %{buildroot}%{_bindir}/xremap-hypr

# Install niri variant
install -D -m 0755 target-niri/release/xremap %{buildroot}%{_bindir}/xremap-niri

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

%post hypr
alternatives --install %{_bindir}/xremap xremap %{_bindir}/xremap-hypr 20

%preun hypr
if [ $1 -eq 0 ]; then
    alternatives --remove xremap %{_bindir}/xremap-hypr
fi

%post niri
alternatives --install %{_bindir}/xremap xremap %{_bindir}/xremap-niri 20

%preun niri
if [ $1 -eq 0 ]; then
    alternatives --remove xremap %{_bindir}/xremap-niri
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

%files hypr
%license LICENSE
%doc README.md
%{_bindir}/xremap-hypr
/usr/lib/udev/rules.d/00-xremap-input.rules

%files niri
%license LICENSE
%doc README.md
%{_bindir}/xremap-niri
/usr/lib/udev/rules.d/00-xremap-input.rules

%changelog
* Wed Dec 10 2025 Blake Gardner <blakerg@gmail.com> - 0.14.6-1
- Update xremap to upstream version 0.14.6

* Fri Nov 28 2025 Blake Gardner <blakerg@gmail.com> - 0.14.5-1
- Update xremap to upstream version 0.14.5

* Fri Nov 28 2025 Blake Gardner <blakerg@gmail.com> - 0.14.4-1
- Update xremap to upstream version 0.14.4

* Mon Nov 03 2025 Blake Gardner <blakerg@gmail.com> - 0.14.3-1
- Update xremap to upstream version 0.14.3

* Mon Nov 03 2025 Blake Gardner <blakerg@gmail.com> - 0.14.2-1
- Update xremap to upstream version 0.14.2

* Thu Sep 26 2025 Blake Gardner <blakerg@gmail.com> - 0.14.1-1
- Update xremap to upstream version 0.14.1

* Mon Sep 22 2025 Blake Gardner <blakerg@gmail.com> - 0.14.0-1
- Update xremap to upstream version 0.14.0

* Tue Sep 16 2025 Blake Gardner <blakerg@gmail.com> - 0.13.0-1
- Update xremap to upstream version 0.13.0

* Mon Sep 15 2025 Blake Gardner <blakerg@gmail.com> - 0.12.0-1
- Update xremap to upstream version 0.12.0

* Sun Sep 14 2025 Blake Gardner <blakerg@gmail.com> - 0.11.0-1
- Update xremap to upstream version 0.11.0

* Thu Sep 12 2025 Blake Gardner <blakerg@gmail.com> - 0.10.18-1
- Update xremap to upstream version 0.10.18

* Thu Sep 4 2025 Blake Gardner <blakerg@gmail.com> - 0.10.16-2
- Added Hyprland and niri package variants

* Thu Sep 4 2025 Blake Gardner <blakerg@gmail.com> - 0.10.16-1
- Update xremap to upstream version 0.10.16

* Tue May 13 2025 Blake Gardner <blakerg@gmail.com> - 0.10.13-1
- Update xremap to upstream version 0.10.13

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
