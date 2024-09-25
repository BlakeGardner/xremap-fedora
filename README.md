

# xremap RPM Package for Fedora

[![Copr build status](https://copr.fedorainfracloud.org/coprs/blakegardner/xremap/package/xremap/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/blakegardner/xremap/package/xremap/)

This repository contains the RPM spec file and packaging scripts for [xremap](https://github.com/xremap/xremap), a key remapper for Linux supporting app-specific remapping and Wayland.

## Installation Instructions

The RPM packages are available via Fedora COPR.

```bash
sudo dnf copr enable blakegardner/xremap
```

## Available Variants

Due to differences in how input events are handled across desktop environments and display servers, `xremap` provides several variants:

- **Vanilla (`xremap`)**: The default build without any specific backend features.
- **GNOME (`xremap-gnome`)**: Built with GNOME Wayland support.
- **X11 (`xremap-x11`)**: Built with X11 support.
- **KDE (`xremap-kde`)**: Built with KDE Plasma Wayland support.
- **wlroots (`xremap-wlroots`)**: Built with wlroots support for compositors like Sway and Hyprland.

**Note:** Only one variant can be installed at a time.

## Switching Between Variants

To switch between different variants of `xremap`, use the `dnf swap` command. This command safely replaces one package with another, handling any conflicts.

```bash
sudo dnf swap xremap-gnome xremap-wlroots
```

## Permissions and Udev Rules

### Input Group

The package creates an `input` group if it doesn't exist. You need to add your user to this group to allow `xremap` to access input devices.

```bash
sudo usermod -aG input $USER
```

Log out and log back in for the group changes to take effect.

### Udev Rules

A udev rules file is installed at `/usr/lib/udev/rules.d/00-xremap-input.rules` to set the appropriate permissions on input devices.
