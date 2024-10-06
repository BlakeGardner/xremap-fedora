

# xremap RPM Package for Fedora

[![Copr build status](https://copr.fedorainfracloud.org/coprs/blakegardner/xremap/package/xremap/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/blakegardner/xremap/package/xremap/)

This repository contains the RPM spec file and packaging scripts for [xremap](https://github.com/xremap/xremap), a key remapper for Linux supporting app-specific remapping and Wayland.

## Installation Instructions

The RPM packages are available via Fedora COPR.

```bash
sudo dnf copr enable blakegardner/xremap
sudo dnf install xremap-gnome
```

## Available Variants

Due to differences in how application specific remapping is implemented in different desktop environments, multiple variants of `xremap` are available. Choose the variant that best matches your desktop environment.

- **Vanilla (`xremap`)**: Use this variant if you're unsure which one to choose.
- **GNOME (`xremap-gnome`)**: This variant is recommended if you want application-specific remapping to work in GNOME.
- **KDE (`xremap-kde`)**: This variant is recommended if you want application-specific remapping to work in KDE Plasma.
- **wlroots (`xremap-wlroots`)**: This variant is recommended if you're using a wlroots-based compositor.
- **X11 (`xremap-x11`)**: This variant is recommended if you're using an X11-based desktop environment.

**Note:** Only one variant can be installed at a time.

## Switching Between Variants

To switch between different variants of `xremap`, use the `dnf swap` command. This command safely replaces one package with another, handling any conflicts.

```bash
sudo dnf swap xremap xremap-gnome
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
