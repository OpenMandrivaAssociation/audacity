%define fversion %{version}

Summary:	Free Audio Editor With Effects/Analysis Tools
Name:		audacity
Version: 	1.3.5
Release: 	%mkrel 1
License: 	GPLv2+
Group: 		Sound
URL: 		http://audacity.sourceforge.net/
Source0: 	http://prdownloads.sourceforge.net/%{name}/%{name}-src-%{fversion}.tar.bz2
Source1:	%{name}_16x16.png
Source2:	%{name}_32x32.png
Source3:	%{name}_64x64.png
Source4:	%{name}.sh
Patch:		audacity-src-1.3.4-beta-desktopentry.patch
Patch5:		audacity-system-libs.patch
Patch7:		audacity-external_portaudio.diff
Patch8:		audacity-1.3.5-CVE-2007-6061.patch
BuildRequires: 	autoconf2.5
BuildRequires:	fftw-devel >= 2.1.4
BuildRequires:	gettext-devel
BuildRequires: 	ImageMagick
BuildRequires: 	libalsa-devel
BuildRequires:  libflac++-devel
BuildRequires:  libid3tag-devel
BuildRequires:	libjpeg-devel
BuildRequires:  libmad-devel
BuildRequires:	libogg-devel
BuildRequires:	resample-devel >= 0.1.3
BuildRequires:	libsndfile-devel
BuildRequires:	libvorbis-devel
BuildRequires:	soundtouch-devel >= 1.3.0
BuildRequires:	speex-devel
BuildRequires:	portaudio-devel
#BuildRequires:	twolame-devel
BuildRequires:	wxgtku2.8-devel
BuildRequires: 	zlib-devel
#for compressing the help file:
BuildRequires:  zip
#gw if regenerating configure
BuildRequires: 	autoconf-archive
Obsoletes:	hackaudacity
Requires(post): shared-mime-info
Requires(postun): shared-mime-info
Requires(post):	desktop-file-utils
Requires(postun):desktop-file-utils
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

%setup -q -n %{name}-src-%{fversion}-beta
%patch -p1 -b .desktopentry
%patch5 -p1 -b .system-libs
%patch7 -p1 -b .portaudio
%patch8 -p1

chmod 644 *.txt
aclocal
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
    --with-libresample \
    --with-id3tag=system \
    --with-soundtouch=system \
    --with-portmixer=system \
    --with-portaudio=system

#    --with-libtwolame=system \

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

# install pasuspender script for audacity
mv %{buildroot}/%{_bindir}/audacity %{buildroot}/%{_bindir}/audacity.bin
install -m755 %{SOURCE4} %{buildroot}/%{_bindir}/audacity


%post
%update_menus
%update_mime_database
%update_desktop_database

%postun
%clean_menus
%clean_mime_database
%clean_desktop_database

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
