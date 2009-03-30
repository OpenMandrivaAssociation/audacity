%define fversion %{version}

Summary:	Free Audio Editor With Effects/Analysis Tools
Name:		audacity
Version: 	1.3.7
Release: 	%mkrel 5
License: 	GPLv2+
Group: 		Sound
URL: 		http://audacity.sourceforge.net/
Source0: 	http://prdownloads.sourceforge.net/%{name}/%{name}-minsrc-%{fversion}.tar.bz2
Source1:	%{name}_16x16.png
Source2:	%{name}_32x32.png
Source3:	%{name}_64x64.png
Patch:		audacity-1.3.6-desktopentry.patch
Patch1:		audacity-src-1.3.7-format-strings.patch
#gw from Fedora, use the right default audio device if using Pulseaudio
Patch2:		audacity-1.3.7-audiodevdefaults.patch
#gw rediffed from Fedora, build with vamp 1.1 
#drop once vamp was updated to 2.0
Patch3:		audacity-1.3.7-vamp-1.3.patch
#gw from Fedora, fix crash in Effect->Repeat
Patch4:		audacity-1.3.7-repeat.patch
Patch5:		audacity-system-libs.patch
#gw use Alsa by default
Patch6:		audacity-src-1.3.7-alsa-by-default.patch
Patch7:		audacity-external_portaudio.diff
Patch8:		audacity-1.3.5-CVE-2007-6061.patch
Patch9:		portaudio-19-alsa_pulse.patch
Patch10:	audacity-1.3.7-CVE-2009-0490.diff
#gw make preferences window resizable
#https://qa.mandriva.com/show_bug.cgi?id=49244
Patch11:	audacity-src-1.3.7-resizable-preferences.patch
BuildRequires: 	autoconf2.5
BuildRequires:	fftw-devel >= 2.1.4
BuildRequires:	gettext-devel
BuildRequires: 	imagemagick
BuildRequires: 	libalsa-devel
BuildRequires:  libflac++-devel
BuildRequires:  libjack-devel
BuildRequires:  libid3tag-devel
BuildRequires:	libjpeg-devel
BuildRequires:  libmad-devel
BuildRequires:	libogg-devel
BuildRequires:  libsamplerate-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libvorbis-devel
BuildRequires:	soundtouch-devel >= 1.3.0
BuildRequires:	speex-devel
#gw 1.3.7 doesn't build with our portaudio lib
#BuildRequires:	portaudio-devel
BuildRequires:	twolame-devel
BuildRequires:	wxgtku2.8-devel
BuildRequires: 	zlib-devel
BuildRequires: 	libffmpeg-devel
BuildRequires:	vamp-plugin-sdk-devel
#gw these are not supported in 1.3.7
#BuildRequires:	liblrdf-devel
#BuildRequires: 	slv2-devel >= 0.6.0-1mdv
BuildRequires: 	libexpat-devel
#for compressing the help file:
BuildRequires:  zip
Obsoletes:	hackaudacity
Requires(post): shared-mime-info
Requires(postun): shared-mime-info
Requires(post):	desktop-file-utils
Requires(postun):desktop-file-utils
Suggests: libffmpeg
Suggests: %mklibname lame 0
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch -p1 -b .desktopentry
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1 -b .system-libs
%patch6 -p1
%patch7 -p1 -b .portaudio
%patch8 -p1
cd lib-src/portaudio-v19/
%patch9 -p1
cd ../..
%patch10 -p0 -b .CVE-2009-0490
%patch11 -p1

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
    --with-portaudio=v19 \
    --with-libtwolame=system \
    --with-ffmpeg
%make

%install
rm -rf %{buildroot} %{name}.lang
%makeinstall_std

%find_lang %{name}

#icon
mkdir -p %{buildroot}/{%{_miconsdir},%{_liconsdir}}
convert -transparent white %{SOURCE1} %{buildroot}%{_miconsdir}/%{name}.png
convert -transparent white %{SOURCE2} %{buildroot}%{_iconsdir}/%{name}.png
cp %{SOURCE3} %{buildroot}%{_liconsdir}/%{name}.png

#clean uneeded installed but not packaged
rm -rf %{buildroot}%{_docdir}/%{name}

%if %mdkversion < 200900
%post
%update_menus
%update_mime_database
%update_desktop_database
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_mime_database
%clean_desktop_database
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc LICENSE.txt README.txt
%{_bindir}/*
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_miconsdir}/*.png
%{_datadir}/audacity
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/audacity.xml
%{_mandir}/man1/audacity.1*
