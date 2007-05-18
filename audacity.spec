%define name	audacity
%define version 1.3.3
%define fversion %version
%define release %mkrel 1

Summary:	Free Audio Editor With Effects/Analysis Tools
Name:		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Sound
URL: 		http://audacity.sourceforge.net/
Source0: 	http://prdownloads.sourceforge.net/%{name}/%{name}-src-%{fversion}.tar.bz2
Source1:	%{name}_16x16.png
Source2:	%{name}_32x32.png
Source3:	%{name}_64x64.png
Patch: audacity-src-1.3.0-beta-xdg.patch
Patch1:		audacity-src-1.3.2-beta-soundtouch-non-x86.patch
Patch2: audacity-src-1.3.3-beta-flac.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	wxgtku-devel < 2.7
BuildRequires:  libflac++-devel
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:  libmad-devel
#BuildRequires:  libid3tag-devel
BuildRequires:	libsndfile-devel
buildrequires: 	zlib-devel
buildrequires: 	libalsa-devel
BuildRequires: 	autoconf2.5
BuildRequires: 	ImageMagick
BuildRequires: 	desktop-file-utils
#for compressing the help file:
BuildRequires:  zip
Obsoletes:	hackaudacity
Requires(post): shared-mime-info
Requires(postun): shared-mime-info
Requires(post):	desktop-file-utils
Requires(postun):desktop-file-utils

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
%patch -p1 -b .xdg
%patch1 -p1 -b .ppc
%patch2 -p1 -b .flac
chmod 644 *.txt
ln -s %_libdir/wx/config/`multiarch-platform`/gtk2-unicode-release-2.6 wx-config
aclocal
autoconf
pushd lib-src/soundtouch
aclocal
automake --foreign
autoconf
popd


%build
export PATH=$PATH:`pwd`
export LDFLAGS=-lz
./configure --prefix=%_prefix --libdir=%_libdir --enable-optimise \
            --with-vorbis=system \
            --with-libmad=system \
	    --with-portaudio=v19 --without-portmixer \
            --with-libsndfile=system
make

%install
rm -rf %buildroot %name.lang
mkdir -p %buildroot/%_bindir
%makeinstall BINDIR=%buildroot%_bindir DATADIR=%buildroot%_datadir MANDIR=%buildroot%_mandir
mv %buildroot%_datadir/locale/zh %buildroot%_datadir/locale/zh_CN


%{find_lang} %{name}

# Menu
mkdir -p %buildroot/%{_menudir}
cat > %buildroot/%{_menudir}/%{name} <<EOF
?package(%{name}): command="%{_bindir}/%{name}" needs="X11" \
icon="%{name}.png" section="Multimedia/Sound" \
title="Audacity" longtitle="Digital audio waveforms editor" xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="Multimedia" \
  --add-category="AudioVideoEditing;Recorder" \
  --add-category="X-MandrivaLinux-Multimedia-Sound" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

#icon
mkdir -p %{buildroot}/{%{_miconsdir},%{_liconsdir}}
convert -transparent white %{SOURCE1} $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
convert -transparent white %{SOURCE2} $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
cp %{SOURCE3} $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png

#clean uneeded installed but not packaged
rm -rf $RPM_BUILD_ROOT/%{_docdir}/%{name}

%clean
rm -rf %buildroot/

%post
%{update_menus}
%update_mime_database
%update_desktop_database

%postun
%{clean_menus}
%clean_mime_database
%clean_desktop_database

%files -f %{name}.lang
%defattr(-,root,root)
%doc LICENSE.txt README.txt
%{_bindir}/*
%{_menudir}/%{name}
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_miconsdir}/*.png
%{_datadir}/audacity
%{_datadir}/applications/%name.desktop
%{_datadir}/mime/packages/audacity.xml
%{_mandir}/man1/audacity.1.bz2


