%define _disable_ld_no_undefined 1
# Muse/Audacity 4 headers construct maps and QLists at namespace scope
# (inline std::string tags, ID_STRINGS, GENERIC_SETUP_DATA, ...). Clang
# LTO reorders those constructors across TUs, so one static copies or
# looks up another before it exists. First crash was SIGSEGV in
# projectmeta.h; with that patched, startup still aborts in
# muse::mpe::soundIdToString (unordered_map::at on an empty ID_STRINGS).
%define _disable_lto 1
# -pthread must be on the PCH as well; wx-config adds it later and Clang
# rejects a PCH that was built without POSIX thread support.
%global optflags %{optflags} -fPIC -pthread
# Upstream installs resources under share/audacity-MAJOR.MINOR
%define majmin %(echo %{version}|cut -d. -f1-2)
# Official tarball already unpacks as audacity-VERSION/; default %%autosetup -C
# would nest that as audacity-VERSION/audacity-VERSION/
%define buildsystem_cmake_prep() %autosetup -p1 -n %{name}-%{version}

Summary:	Free Audio Editor With Effects/Analysis Tools
Name:		audacity
Version:	4.0.0
Release:	2
License:	GPLv3
Group:		Sound
URL:		https://www.audacityteam.org/
Source0:	https://github.com/audacity/audacity/releases/download/Audacity-%{version}/audacity-sources-%{version}.tar.xz
Source100:	%{name}.rpmlintrc
# Clang rejects the NEON float32x4_t aggregate init used by StaffPad
Patch0:		audacity-4.0.0-neon-clang.patch
# Upstream desktop Name is always "... Portable" (AppImage leftover)
Patch1:		audacity-4.0.0-desktop-name.patch
# qt_standard_project_setup SUPPORTS_UP_TO 6.10 warns on cooker Qt 6.11
Patch2:		audacity-4.0.0-qt-6.11.patch
# Header-scope std::string / muse::trc statics crash before main with clang+LTO
Patch3:		audacity-4.0.0-static-init.patch

BuildSystem:	cmake
# Official snapshot ships dependency sources in offline-deps/ (no network at build time)
BuildOption:	-DEXTDEPS_CACHE=%{_builddir}/%{name}-%{version}/offline-deps
# Use system copies of expat/flac/portaudio/wxBase/...; in-tree source-only
# deps (Nyquist, VST3 SDK, LV2, soxr, sbsms, ...) still rebuild from offline-deps
BuildOption:	-DEXTDEPS_OVERRIDE_ALL=SYSTEM
BuildOption:	-DAU4_BUILD_MODE=release
BuildOption:	-DAU4_BUILD_CONFIGURATION=app
BuildOption:	-DMUSE_ENABLE_UNIT_TESTS:BOOL=OFF
BuildOption:	-DMUSE_MODULE_DIAGNOSTICS_CRASHPAD_CLIENT:BOOL=OFF
BuildOption:	-DMUSE_MODULE_UPDATE:BOOL=OFF
BuildOption:	-DAU_BUILD_USAGEINFO_MODULE:BOOL=OFF
BuildOption:	-DAU_USE_SBSMS:BOOL=ON
BuildOption:	-DAU_USE_SOUNDTOUCH:BOOL=ON

BuildRequires:	git
BuildRequires:	desktop-file-utils
# Needed at build time so we can symlink the catalogues the app loads from its locale dir
BuildRequires:	qt6-qttranslations
BuildRequires:	atomic-devel
BuildRequires:	ffmpeg-devel
# au3 still links wxBase only. Cooker wxQt 3.2 is built against Qt 5 and would
# pull Qt5Core into this Qt 6 app; wxGTK's wx-config --libs base is just libwx_baseu.
BuildRequires:	wxgtk-devel
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6CorePrivate)
BuildRequires:	cmake(Qt6GuiPrivate)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6NetworkAuth)
BuildRequires:	cmake(Qt6Qml)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6QuickControls2)
BuildRequires:	cmake(Qt6QuickWidgets)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6PrintSupport)
BuildRequires:	cmake(Qt6ShaderTools)
BuildRequires:	cmake(Qt6Core5Compat)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6StateMachine)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(utf8cpp)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(flac++)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(harfbuzz)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libmpg123)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(opusfile)
BuildRequires:	pkgconfig(pugixml)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(wavpack) >= 5.2.0
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	lame-devel

# QML plugins and image format plugins are loaded at runtime
Requires:	qt6-qtdeclarative
Requires:	qt6-qtimageformats
# Symlinked into share/audacity-%%{majmin}/locale (the app does not search the system Qt path)
Requires:	qt6-qttranslations

%description
Audacity is a program that lets you manipulate digital audio waveforms.

In addition to letting you record sounds directly from within the program,
it imports many sound file formats, including WAV, AIFF, MP3 and Ogg/Vorbis.
It supports all common editing operations such as Cut, Copy, and Paste, plus
it will mix tracks and let you apply plug-in effects to any part of a sound.
It also has a built-in amplitude envelope editor, a customizable spectrogram
mode and a frequency analysis window for audio analysis applications.

Audacity 4 rebuilds the interface on Qt 6. The audio engine is still the
Audacity 3 codebase, wrapped for the new frontend.

%install -a
desktop-file-install \
	--add-category="Qt" \
	--add-category="X-MandrivaLinux-CrossDesktop" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

# muse_deps may drop rebuilt-dep licenses under /usr/licenses
rm -rf %{buildroot}/usr/licenses
rm -rf %{buildroot}%{_docdir}/%{name}

# Upstream copies Qt's catalogues next to Audacity's .qm files. Replace
# those copies with symlinks so a qt6-qttranslations update is picked up.
for f in %{buildroot}%{_datadir}/%{name}-%{majmin}/locale/qt_*.qm \
	%{buildroot}%{_datadir}/%{name}-%{majmin}/locale/qtbase_*.qm; do
	[ -e "$f" ] || continue
	bn="${f##*/}"
	rm -f "$f"
	ln -s %{_qtdir}/translations/"$bn" "$f"
done

%files
%doc LICENSE.txt README.md
%{_bindir}/audacity
%{_datadir}/applications/org.audacityteam.Audacity.desktop
%{_datadir}/metainfo/org.audacityteam.Audacity.appdata.xml
%{_datadir}/mime/packages/audacity.xml
%{_datadir}/icons/hicolor/*/apps/audacity.png
%{_datadir}/icons/hicolor/512x512/mimetypes/application-x-audacity.png
%{_datadir}/icons/hicolor/scalable/mimetypes/application-x-audacity.svg
%{_datadir}/audacity
%{_datadir}/%{name}-%{majmin}
