Summary:	Free Audio Editor With Effects/Analysis Tools
Name:		audacity
Version:	2.1.0
Release:	5
License:	GPLv2+
Group:		Sound
Url:		http://audacity.sourceforge.net/
Source0:	http://audacity.googlecode.com/files/audacity-minsrc-%{version}.tar.xz
# Was needed for 2.1.0
Source1:	audacity_ru.mo
Patch0:		audacity-2.1.0-ffmpeg2.4.patch
BuildRequires:	autoconf2.5
BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
#for compressing the help file:
BuildRequires:	zip
BuildRequires:	ffmpeg-devel
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

%files -f %{name}.lang
%doc LICENSE.txt README.txt
%{_bindir}/*
%{_datadir}/audacity/
%{_datadir}/appdata/audacity.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/audacity.*
%{_datadir}/pixmaps/*
%{_datadir}/mime/packages/audacity.xml
%{_mandir}/man1/audacity.1*

#----------------------------------------------------------------------------

%prep
%setup -qn %{name}-minsrc-%{version}
%patch0 -p0

rm -rf lib-src/ffmpeg

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

rm -rf %{buildroot}%{_datadir}/locale/ru/LC_MESSAGES/audacity.mo
cp %{SOURCE1} %{buildroot}%{_datadir}/locale/ru/LC_MESSAGES/audacity.mo

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

