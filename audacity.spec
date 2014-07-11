%define fversion %{version}

Summary:	Free Audio Editor With Effects/Analysis Tools
Name:		audacity
Version:	2.0.5
Release:	3
License:	GPLv2+
Group:		Sound
URL:		http://audacity.sourceforge.net/
Source0:	http://audacity.googlecode.com/files/audacity-minsrc-%{version}.tar.xz
#Patch5:		audacity-system-libs.patch
#gw use Alsa by default
#Patch6:		audacity-1.3.8-alsa-by-default.patch
#Patch8:		audacity-1.3.14-CVE-2007-6061.patch
#Patch10:	audacity-1.3.7-CVE-2009-0490.diff
Patch11:	audacity-2.0.0-fix-linking.patch
BuildRequires:	autoconf2.5
BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
#for compressing the help file:
BuildRequires:	zip
BuildRequires:	ffmpeg0.7-devel
BuildRequires:	gettext-devel
BuildRequires:	jpeg-devel
BuildRequires:	wxgtku2.8-devel >= 2.8.10
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(flac++)
BuildRequires:	pkgconfig(id3tag)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(soundtouch)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(twolame)
BuildRequires:	pkgconfig(vamp-sdk)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(zlib)

%description
Audacity is a program that lets you manipulate digital audio waveforms.

In addition to letting you record sounds directly from within the program,
it imports many sound file formats, including WAV, AIFF, MP3 and Ogg/Vorbis.
It supports all common editing operations such as Cut, Copy, and Paste, plus
it will mix tracks and let you apply plug-in effects to any part of a sound.
It also has a built-in amplitude envelope editor, a customizable spectrogram
mode and a frequency analysis window for audio analysis applications.

%prep
%setup -q -n %{name}-src-%{fversion}
#%patch5 -p1 -b .system-libs
#%patch6 -p1 -b .alsa-by-default
#%patch8 -p1
#%patch10 -p0 -b .CVE-2009-0490
%patch11 -p1 -b .linking

chmod 644 *.txt
aclocal -I m4
autoconf

%build
export PATH=$PATH:`pwd`
export LDFLAGS=-lz
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"

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
%make

%install
%makeinstall_std

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
%{_datadir}/audacity
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/audacity.*
%{_datadir}/pixmaps/*
%{_datadir}/mime/packages/audacity.xml
%{_mandir}/man1/audacity.1*



