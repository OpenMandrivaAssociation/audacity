%define fversion %{version}
%define oname   Audacity
%define _disable_lto 1

Summary:	Free Audio Editor With Effects/Analysis Tools
Name:		audacity
Version:	2.4.0
Release:	1
License:	GPLv2+
Group:		Sound
URL:		https://www.audacityteam.org/
Source0:  https://github.com/audacity/audacity/archive/Audacity-%{version}/%{name}-%{oname}-%{version}.tar.gz
# As of 2.4.0 Audacity from audacity website not contains configure. So, we switch source to GitHub
#Source0:	https://www.fosshub.com/Audacity.html/audacity-minsrc-%{version}.tar.xz
Source100:	%{name}.rpmlintrc
#Patch1:		audacity-ffmpeg.patch
BuildRequires:	autoconf2.5
BuildRequires:  cmake
BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:  lame-devel
#for compressing the help file:
BuildRequires:	zip
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext-devel
BuildRequires:	jpeg-devel
# Is in unsupported. So leave it disable
#BuildRequires:  portmidi-devel
BuildRequires:	wxgtku3.0-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(flac++)
BuildRequires:	pkgconfig(id3tag)
BuildRequires:	pkgconfig(jack)
BuildRequires:  pkgconfig(lv2)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(soundtouch)
BuildRequires:	pkgconfig(speex)
BuildRequires:  pkgconfig(soxr)
BuildRequires:	pkgconfig(twolame)
BuildRequires:	pkgconfig(vamp-sdk)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(zlib)
BuildRequires:  pkgconfig(python)
BuildRequires:  pkgconfig(portaudio-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)

%description
Audacity is a program that lets you manipulate digital audio waveforms.

In addition to letting you record sounds directly from within the program,
it imports many sound file formats, including WAV, AIFF, MP3 and Ogg/Vorbis.
It supports all common editing operations such as Cut, Copy, and Paste, plus
it will mix tracks and let you apply plug-in effects to any part of a sound.
It also has a built-in amplitude envelope editor, a customizable spectrogram
mode and a frequency analysis window for audio analysis applications.

%prep
%setup -q -n %{name}-%{oname}-%{fversion}
#autopatch -p1
chmod 644 *.txt

%build
#export PATH=$PATH:`pwd`
#export LDFLAGS=-lz
#export CFLAGS="%{optflags}"
#export CXXFLAGS="%{optflags}"
#export CC=%__cc
#export CXX=%__cxx
#export OBJCXX=%__cxx
#export LD=%__cxx

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --enable-optimise \
    --enable-unicode \
    --with-vorbis=system \
    --with-libmad=system \
    --with-libsndfile=system \
    --with-libsamplerate \
    --with-id3tag=system \
    --with-soundtouch=system \
    --with-portmixer \
    --with-portaudio \
    --with-libtwolame=system \
    --with-ffmpeg
%make_build

%install
%make_install

%find_lang %{name}

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
%doc LICENSE.txt README.txt
%{_bindir}/*
%{_libdir}/audacity/libsuil_x11.so
%{_libdir}/audacity/libsuil_x11_in_gtk3.so
%{_datadir}/audacity
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/audacity.*
%{_datadir}/pixmaps/*
%{_datadir}/appdata/audacity.appdata.xml
%{_datadir}/mime/packages/audacity.xml
%{_mandir}/man1/audacity.1*
