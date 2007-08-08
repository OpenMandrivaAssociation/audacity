%define fversion %{version}

Summary:	Free Audio Editor With Effects/Analysis Tools
Name:		audacity
Version: 	1.3.3
Release: 	%mkrel 2
License: 	GPL
Group: 		Sound
URL: 		http://audacity.sourceforge.net/
Source0: 	http://prdownloads.sourceforge.net/%{name}/%{name}-src-%{fversion}.tar.bz2
Source1:	%{name}_16x16.png
Source2:	%{name}_32x32.png
Source3:	%{name}_64x64.png
Patch0:		audacity-src-1.3.0-beta-xdg.patch
Patch1:		audacity-src-1.3.2-beta-soundtouch-non-x86.patch
Patch2:		audacity-src-1.3.3-beta-flac.patch
Patch3:		audacity-not_require_lame-libs-devel.patch
Patch4:		audacity-not_require_lame-libs-devel-generated_part.patch
Patch5:		audacity-system-libs.patch
Patch6:		audacity-opt.patch
Patch7:		audacity-external_portaudio.diff
BuildRequires: 	autoconf2.5
BuildRequires: 	desktop-file-utils
BuildRequires:	fftw-devel >= 2.1.4
BuildRequires:	gettext-devel
BuildRequires: 	ImageMagick
BuildRequires: 	libalsa-devel
BuildRequires:  libflac++-devel
BuildRequires:  libid3tag-devel
BuildRequires:  libjack-devel
BuildRequires:	libjpeg-devel
BuildRequires:  libmad-devel
BuildRequires:	libogg-devel
BuildRequires:	resample-devel >= 0.1.3
BuildRequires:	libsndfile-devel
BuildRequires:	libvorbis-devel
BuildRequires:	soundtouch-devel >= 1.3.0
BuildRequires:	speex-devel
#BuildRequires:	twolame-devel
BuildRequires:	wxgtku-devel < 2.7
BuildRequires:	wxGTK2.6-devel
BuildRequires: 	zlib-devel
#for compressing the help file:
BuildRequires:  zip
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
%patch0 -p1 -b .xdg
%patch1 -p1 -b .ppc
%patch2 -p1 -b .flac
%patch3 -p1
%patch4 -p0
%patch5 -p1
%patch6 -p1
%patch7 -p0

chmod 644 *.txt
ln -s %{_libdir}/wx/config/`multiarch-platform`/gtk2-unicode-release-2.6 wx-config
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
    --with-wx-version=2.6 \
    --enable-unicode \
    --with-vorbis=system \
    --with-libmad=system \
    --with-libsndfile=system \
    --with-libresample=system \
    --with-id3tag=system \
    --with-soundtouch=system \
    --with-portmixer=system \
    --with-portaudio=system

#    --with-libtwolame=system \

%make

%install
rm -rf %{buildroot} %{name}.lang
mkdir -p %{buildroot}/%{_bindir}

%makeinstall BINDIR=%{buildroot}%{_bindir} DATADIR=%{buildroot}%{_datadir} MANDIR=%{buildroot}%{_mandir}

mv %{buildroot}%{_datadir}/locale/zh %{buildroot}%{_datadir}/locale/zh_CN


%find_lang %{name}

# Menu
mkdir -p %{buildroot}/%{_menudir}
cat > %{buildroot}/%{_menudir}/%{name} <<EOF
?package(%{name}): command="%{_bindir}/%{name}" needs="X11" \
icon="%{name}.png" section="Multimedia/Sound" \
title="Audacity" longtitle="Digital audio waveforms editor" xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="Multimedia" \
  --add-category="AudioVideoEditing;Recorder" \
  --add-category="X-MandrivaLinux-Multimedia-Sound" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

#icon
mkdir -p %{buildroot}/{%{_miconsdir},%{_liconsdir}}
convert -transparent white %{SOURCE1} %{buildroot}%{_miconsdir}/%{name}.png
convert -transparent white %{SOURCE2} %{buildroot}%{_iconsdir}/%{name}.png
cp %{SOURCE3} %{buildroot}%{_liconsdir}/%{name}.png

#clean uneeded installed but not packaged
rm -rf %{buildroot}%{_docdir}/%{name}

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
%{_menudir}/%{name}
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_miconsdir}/*.png
%{_datadir}/audacity
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/audacity.xml
%{_mandir}/man1/audacity.1*
