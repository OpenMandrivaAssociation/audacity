%define oname   Audacity
%define _disable_lto 1
%define _disable_ld_no_undefined 1
%global _cmake_skip_rpath %{nil}
%global optflags %{optflags} -fPIC
#define gitdate 20240605

Summary:	Free Audio Editor With Effects/Analysis Tools
Name:		audacity
Version:	3.7.4
Release:	%{?gitdate:0.%{gitdate}.}3
License:	GPLv2+
Group:		Sound
URL:		https://www.audacityteam.org/
%if ! 0%{?gitdate:1}
Source0:	https://github.com/audacity/audacity/archive/%{name}-Audacity-%{version}.tar.gz
%else
Source0:	https://github.com/audacity/audacity/archive/refs/heads/master.tar.gz#/%{name}-%{gitdate}.tar.gz
%endif
Source100:	%{name}.rpmlintrc
#Patch0:         audacity-2.4.2-default-theme-dark.patch
#Patch1:         system-wx.patch
#Patch2:         0001-Fix-compilation-with-llvm-11.0.1.patch
#Patch3:		audacity-workaround-clang-bug-50230.patch
Patch3:		audacity-3.4.0-fix-build.patch
Patch4:		audacity-3.0.2-no-x86-hardcodes.patch
Patch5:		rpath-openmandriva.patch
Patch6:		audacity-3.6.0-bug-4614.patch
Patch7:		audacity-non-x86.patch
Patch8:		audacity-rapidjson-1.2.patch

#BuildRequires:  git
BuildRequires:	ninja
BuildRequires:  cmake
BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:  lame-devel
#for compressing the help file:
BuildRequires:	zip
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext-devel
BuildRequires:	jpeg-devel
BuildRequires:	atomic-devel
BuildRequires:  portmidi-devel
BuildRequires:	libwxgtk3.2-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(flac++)
BuildRequires:	pkgconfig(id3tag)
BuildRequires:	pkgconfig(jack)
BuildRequires:  pkgconfig(lv2)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(opusfile)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(soundtouch)
BuildRequires:	pkgconfig(speex)
BuildRequires:  pkgconfig(soxr)
BuildRequires:	pkgconfig(suil-0)
BuildRequires:	pkgconfig(lilv-0)
BuildRequires:	pkgconfig(serd-0)
BuildRequires:	pkgconfig(sord-0)
BuildRequires:	pkgconfig(sratom-0)
BuildRequires:	pkgconfig(twolame)
BuildRequires:	pkgconfig(vamp-sdk)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(zlib)
BuildRequires:  pkgconfig(python)
BuildRequires:  pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(wavpack) >= 5.2.0
BuildRequires:	lame-devel
BuildRequires:	pkgconfig(libmpg123)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk+-x11-3.0)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(RapidJSON)
#BuildRequires:	vst3sdk

%description
Audacity is a program that lets you manipulate digital audio waveforms.

In addition to letting you record sounds directly from within the program,
it imports many sound file formats, including WAV, AIFF, MP3 and Ogg/Vorbis.
It supports all common editing operations such as Cut, Copy, and Paste, plus
it will mix tracks and let you apply plug-in effects to any part of a sound.
It also has a built-in amplitude envelope editor, a customizable spectrogram
mode and a frequency analysis window for audio analysis applications.

%prep
%autosetup -p1 -n audacity%{?gitdate:-master}%{!?gitdate:-Audacity-%{version}}
chmod 644 *.txt

%build
# As of Clang 18 and Audacity 3.6.0, app compiled with Clang no longer launching. No errors that would give some guess. Switch to GCC for now.
export CC=gcc
export CXX=g++
[ ! -f src/RevisionIdent.h ] && echo ' ' > src/RevisionIdent.h
# sbsms uses x86 inline assembly
%cmake \
        -DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_SKIP_RPATH:BOOL=OFF \
	-Daudacity_use_pch:BOOL=OFF \
	-Daudacity_obey_system_dependencies=ON \
	-Daudacity_conan_enabled=off \
	-Daudacity_use_portsmf=local \
	-Daudacity_use_ffmpeg=loaded \
	-Daudacity_use_lame=system \
	-Daudacity_use_midi=system \
	-Daudacity_use_portsmf=local \
	-Daudacity_has_vst3:BOOL=OFF \
	-DwxWidgets_CONFIG_EXECUTABLE:FILEPATH=%{_bindir}/wx-config-3.2 \
%ifarch %{x86_64}
	-Daudacity_use_sbsms=local \
%endif
	-Daudacity_use_wxwidgets=system \
	-G Ninja
	
%ninja_build

%install
%ninja_install -C build

%find_lang %{name}

rm -f %{buildroot}/usr/%{name}

#clean uneeded installed but not packaged
rm -rf %{buildroot}%{_docdir}/%{name}

#gw work around bug #52526
mkdir -p %{buildroot}%{_datadir}/%{name}/help/manual

desktop-file-install \
        --add-category="GTK" \
        --add-category="X-MandrivaLinux-CrossDesktop" \
        --dir %{buildroot}%{_datadir}/applications \
        %{buildroot}%{_datadir}/applications/*

%files -f %{name}.lang
%doc LICENSE.txt README*
%{_bindir}/*
%{_libdir}/%{name}/lib*
%{_libdir}/audacity/modules/mod*
%{_datadir}/audacity
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/audacity.*
%{_datadir}/icons/hicolor/*x*/audacity.png
%{_datadir}/pixmaps/*
%{_datadir}/metainfo/audacity.appdata.xml
%{_datadir}/mime/packages/audacity.xml
%{_mandir}/man1/audacity.1*
