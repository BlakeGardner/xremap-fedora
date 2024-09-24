Name:           xremap
Version:        0.10.1
Release:        1%{?dist}
Summary:        A key remapper for X11 and Wayland

License:        MIT
URL:            https://github.com/xremap/xremap
Source0:        https://github.com/xremap/xremap/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  rust, cargo
Conflicts:      %{name}-gnome, %{name}-x11, %{name}-kde, %{name}-wlroots

%description
xremap is a key remapper for Linux. It supports app-specific remapping and Wayland.

### **Subpackage: GNOME**
%package gnome
Summary:        xremap with GNOME Wayland support
Conflicts:      %{name}, %{name}-gnome-debug, %{name}-x11, %{name}-kde, %{name}-wlroots
Requires:       gnome-shell

%description gnome
This version of xremap is built with GNOME Wayland support. You must have the xremap gnome shell extension to use app-specific remapping.

### **Subpackage: X11**
%package x11
Summary:        xremap with X11 support
Conflicts:      %{name}, %{name}-x11-debug, %{name}-gnome, %{name}-kde, %{name}-wlroots

%description x11
This version of xremap is built with X11 support.

### **Subpackage: KDE**
%package kde
Summary:        xremap with KDE-Plasma Wayland support
Conflicts:      %{name}, %{name}-kde-debug, %{name}-gnome, %{name}-x11, %{name}-wlroots
Requires:       plasma-workspace

%description kde
This version of xremap is built with KDE-Plasma Wayland support.

### **Subpackage: wlroots**
%package wlroots
Summary:        xremap with wlroots support (Sway, Hyprland, etc.)
Conflicts:      %{name}, %{name}-wlroots-debug, %{name}-gnome, %{name}-x11, %{name}-kde

%description wlroots
This version of xremap is built with wlroots support (Sway, Hyprland, etc.).

### **Debug Subpackage: Base**
%package debug
Summary:        Debug version of xremap
Conflicts:      %{name}, %{name}-gnome, %{name}-x11, %{name}-kde, %{name}-wlroots
Provides:       %{name} = %{version}-%{release}

%description debug
This package contains the debug version of xremap built without optimizations.

### **Debug Subpackage: GNOME**
%package gnome-debug
Summary:        Debug version of xremap with GNOME Wayland support
Conflicts:      %{name}, %{name}-gnome, %{name}-x11, %{name}-kde, %{name}-wlroots
Requires:       gnome-shell
Provides:       %{name} = %{version}-%{release}

%description gnome-debug
This package contains the debug version of xremap with GNOME Wayland support built without optimizations.

### **Debug Subpackage: X11**
%package x11-debug
Summary:        Debug version of xremap with X11 support
Conflicts:      %{name}, %{name}-gnome, %{name}-x11, %{name}-kde, %{name}-wlroots

%description x11-debug
This package contains the debug version of xremap with X11 support built without optimizations.

### **Debug Subpackage: KDE**
%package kde-debug
Summary:        Debug version of xremap with KDE-Plasma Wayland support
Conflicts:      %{name}, %{name}-gnome, %{name}-x11, %{name}-kde, %{name}-wlroots
Requires:       plasma-workspace

%description kde-debug
This package contains the debug version of xremap with KDE-Plasma Wayland support built without optimizations.

### **Debug Subpackage: wlroots**
%package wlroots-debug
Summary:        Debug version of xremap with wlroots support
Conflicts:      %{name}, %{name}-gnome, %{name}-x11, %{name}-kde, %{name}-wlroots

%description wlroots-debug
This package contains the debug version of xremap with wlroots support built without optimizations.

%prep
%autosetup -n %{name}-%{version}

%build
# Build the release versions
export RUSTFLAGS="-C debuginfo=2 -C opt-level=3"
cargo build --release

cargo build --release --features gnome --target-dir target-gnome-release
cargo build --release --features x11 --target-dir target-x11-release
cargo build --release --features kde --target-dir target-kde-release
cargo build --release --features wlroots --target-dir target-wlroots-release

# Build the debug versions
export RUSTFLAGS="-C debuginfo=2 -C opt-level=0"
cargo build

cargo build --features gnome --target-dir target-gnome-debug
cargo build --features x11 --target-dir target-x11-debug
cargo build --features kde --target-dir target-kde-debug
cargo build --features wlroots --target-dir target-wlroots-debug

%install
rm -rf %{buildroot}

# Install the release binaries
install -D -m 0755 target/release/xremap %{buildroot}%{_bindir}/xremap

install -D -m 0755 target-gnome-release/release/xremap %{buildroot}%{_bindir}/xremap-gnome
install -D -m 0755 target-x11-release/release/xremap %{buildroot}%{_bindir}/xremap-x11
install -D -m 0755 target-kde-release/release/xremap %{buildroot}%{_bindir}/xremap-kde
install -D -m 0755 target-wlroots-release/release/xremap %{buildroot}%{_bindir}/xremap-wlroots

# Install the debug binaries (to separate paths)
install -D -m 0755 target/debug/xremap %{buildroot}%{_bindir}/xremap-debug

install -D -m 0755 target-gnome-debug/debug/xremap %{buildroot}%{_bindir}/xremap-gnome-debug
install -D -m 0755 target-x11-debug/debug/xremap %{buildroot}%{_bindir}/xremap-x11-debug
install -D -m 0755 target-kde-debug/debug/xremap %{buildroot}%{_bindir}/xremap-kde-debug
install -D -m 0755 target-wlroots-debug/debug/xremap %{buildroot}%{_bindir}/xremap-wlroots-debug

%files
%license LICENSE
%doc README.md
%{_bindir}/xremap

%files gnome
%license LICENSE
%doc README.md
%{_bindir}/xremap
%{_bindir}/xremap-gnome

%post gnome
cp -f %{_bindir}/xremap-gnome %{_bindir}/xremap

%postun gnome
if [ $1 -eq 0 ]; then
    rm -f %{_bindir}/xremap
fi

%files x11
%license LICENSE
%doc README.md
%{_bindir}/xremap
%{_bindir}/xremap-x11

%post x11
cp -f %{_bindir}/xremap-x11 %{_bindir}/xremap

%postun x11
if [ $1 -eq 0 ]; then
    rm -f %{_bindir}/xremap
fi

%files kde
%license LICENSE
%doc README.md
%{_bindir}/xremap
%{_bindir}/xremap-kde

%post kde
cp -f %{_bindir}/xremap-kde %{_bindir}/xremap

%postun kde
if [ $1 -eq 0 ]; then
    rm -f %{_bindir}/xremap
fi

%files wlroots
%license LICENSE
%doc README.md
%{_bindir}/xremap
%{_bindir}/xremap-wlroots

%post wlroots
cp -f %{_bindir}/xremap-wlroots %{_bindir}/xremap

%postun wlroots
if [ $1 -eq 0 ]; then
    rm -f %{_bindir}/xremap
fi

%files debug
%license LICENSE
%doc README.md
%{_bindir}/xremap-debug

%post debug
cp -f %{_bindir}/xremap-debug %{_bindir}/xremap

%postun debug
if [ $1 -eq 0 ]; then
    rm -f %{_bindir}/xremap
fi

%files gnome-debug
%license LICENSE
%doc README.md
%{_bindir}/xremap-debug
%{_bindir}/xremap-gnome-debug

%post gnome-debug
cp -f %{_bindir}/xremap-gnome-debug %{_bindir}/xremap

%postun gnome-debug
if [ $1 -eq 0 ]; then
    rm -f %{_bindir}/xremap
fi

%files x11-debug
%license LICENSE
%doc README.md
%{_bindir}/xremap-debug
%{_bindir}/xremap-x11-debug

%post x11-debug
cp -f %{_bindir}/xremap-x11-debug %{_bindir}/xremap

%postun x11-debug
if [ $1 -eq 0 ]; then
    rm -f %{_bindir}/xremap
fi

%files kde-debug
%license LICENSE
%doc README.md
%{_bindir}/xremap-debug
%{_bindir}/xremap-kde-debug

%post kde-debug
cp -f %{_bindir}/xremap-kde-debug %{_bindir}/xremap

%postun kde-debug
if [ $1 -eq 0 ]; then
    rm -f %{_bindir}/xremap
fi

%files wlroots-debug
%license LICENSE
%doc README.md
%{_bindir}/xremap-debug
%{_bindir}/xremap-wlroots-debug

%post wlroots-debug
cp -f %{_bindir}/xremap-wlroots-debug %{_bindir}/xremap

%postun wlroots-debug
if [ $1 -eq 0 ]; then
    rm -f %{_bindir}/xremap
fi

%changelog
* Tue Sep 24 2024 Blake Gardner <blakerg@gmail.com> - 0.10.1-1
- Adjusted spec to build and include both release and debug versions of xremap.
