Name:           xremap
Version:        0.10.1
Release:        1%{?dist}
%define _debugsource_template %{nil}
Summary:        A key remapper for Linux supporting app-specific remapping and Wayland.

License:        MIT
URL:            https://github.com/xremap/xremap
Source0:        https://github.com/xremap/xremap/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  rust, cargo

%description
xremap is a key remapper for Linux. It supports app-specific remapping and Wayland.

### **Subpackage: GNOME**
%package gnome
Summary:        xremap with GNOME Wayland support
Conflicts:      %{name}, %{name}-x11, %{name}-kde, %{name}-wlroots
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} < %{version}-%{release}
Requires:       gnome-shell

%description gnome
This variant of xremap is built with GNOME Wayland support.

### **Subpackage: X11**
%package x11
Summary:        xremap with X11 support
Conflicts:      %{name}, %{name}-gnome, %{name}-kde, %{name}-wlroots
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} < %{version}-%{release}
Requires:       xorg-x11-server-Xorg

%description x11
This variant of xremap is built with X11 support.

### **Subpackage: KDE**
%package kde
Summary:        xremap with KDE Plasma Wayland support
Conflicts:      %{name}, %{name}-gnome, %{name}-x11, %{name}-wlroots
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} < %{version}-%{release}
Requires:       plasma-workspace

%description kde
This variant of xremap is built with KDE Plasma Wayland support.

### **Subpackage: wlroots**
%package wlroots
Summary:        xremap with wlroots support (Sway, Hyprland, etc.)
Conflicts:      %{name}, %{name}-gnome, %{name}-x11, %{name}-kde
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} < %{version}-%{release}

%description wlroots
This variant of xremap is built with wlroots support for compositors like Sway and Hyprland.

%prep
%autosetup -n %{name}-%{version}

%build
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

# Install GNOME variant
install -D -m 0755 target-gnome/release/xremap %{buildroot}%{_bindir}/xremap-gnome

# Install X11 variant
install -D -m 0755 target-x11/release/xremap %{buildroot}%{_bindir}/xremap-x11

# Install KDE variant
install -D -m 0755 target-kde/release/xremap %{buildroot}%{_bindir}/xremap-kde

# Install wlroots variant
install -D -m 0755 target-wlroots/release/xremap %{buildroot}%{_bindir}/xremap-wlroots

%files gnome
%license LICENSE
%doc README.md
%{_bindir}/xremap-gnome

%post gnome
ln -sf %{_bindir}/xremap-gnome %{_bindir}/xremap

%postun gnome
if [ $1 -eq 0 ]; then
    rm -f %{_bindir}/xremap
fi

%files x11
%license LICENSE
%doc README.md
%{_bindir}/xremap-x11

%post x11
ln -sf %{_bindir}/xremap-x11 %{_bindir}/xremap

%postun x11
if [ $1 -eq 0 ]; then
    rm -f %{_bindir}/xremap
fi

%files kde
%license LICENSE
%doc README.md
%{_bindir}/xremap-kde

%post kde
ln -sf %{_bindir}/xremap-kde %{_bindir}/xremap

%postun kde
if [ $1 -eq 0 ]; then
    rm -f %{_bindir}/xremap
fi

%files wlroots
%license LICENSE
%doc README.md
%{_bindir}/xremap-wlroots

%post wlroots
ln -sf %{_bindir}/xremap-wlroots %{_bindir}/xremap

%postun wlroots
if [ $1 -eq 0 ]; then
    rm -f %{_bindir}/xremap
fi

%changelog
* Tue Sep 24 2024 Blake Gardner <blakerg@gmail.com> - 0.10.1-1
- Corrected macro to disable debugsource package generation, resolving build error.
