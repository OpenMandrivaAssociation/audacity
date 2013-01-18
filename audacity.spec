%define fversion %{version}

Summary:	Free Audio Editor With Effects/Analysis Tools
Name:		audacity
Version: 	2.0.2
Release: 	%mkrel 1
License: 	GPLv2+
Group: 		Sound
URL: 		http://audacity.sourceforge.net/
Source0: 	http://audacity.googlecode.com/files/%{name}-minsrc-%{fversion}.tar.bz2
Patch5:		audacity-system-libs.patch
#gw use Alsa by default
Patch6:		audacity-1.3.8-alsa-by-default.patch
Patch8:		audacity-1.3.14-CVE-2007-6061.patch
Patch10:	audacity-1.3.7-CVE-2009-0490.diff
Patch11:	audacity-2.0.0-fix-linking.patch
BuildRequires: 	autoconf2.5
BuildRequires:	fftw-devel >= 2.1.4
BuildRequires:	gettext-devel
BuildRequires: 	imagemagick
BuildRequires: 	libalsa-devel
BuildRequires:  libflac++-devel
BuildRequires:  jackit-devel
BuildRequires:  libid3tag-devel
BuildRequires:	libjpeg-devel
BuildRequires:  libmad-devel
BuildRequires:	libogg-devel
BuildRequires:  libsamplerate-devel
BuildRequires:	sndfile-devel
BuildRequires:	libvorbis-devel
BuildRequires:	soundtouch-devel >= 1.3.0
BuildRequires:	speex-devel
BuildRequires:	twolame-devel
BuildRequires:	wxgtku2.8-devel >= 2.8.10
BuildRequires: 	zlib-devel
%if %mdvver >= 201200
BuildRequires:  ffmpeg0.7-devel
%else
BuildRequires: 	ffmpeg-devel
%endif
BuildRequires:	vamp-plugin-sdk-devel
#gw these are not supported in 1.3.7
#BuildRequires:	liblrdf-devel
#BuildRequires: 	slv2-devel >= 0.6.0-1mdv
BuildRequires: 	expat-devel
BuildRequires: 	desktop-file-utils
#for compressing the help file:
BuildRequires:  zip
Obsoletes:	hackaudacity
Requires(post): shared-mime-info
Requires(postun): shared-mime-info
Requires(post):	desktop-file-utils
Requires(postun):desktop-file-utils
Suggests: libffmpeg
Suggests: %mklibname lame 0

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
%patch5 -p1 -b .system-libs
%patch6 -p1 -b .alsa-by-default
%patch8 -p1
%patch10 -p0 -b .CVE-2009-0490
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
rm -rf %{buildroot} %{name}.lang
%makeinstall_std

%find_lang %{name}

#clean uneeded installed but not packaged
rm -rf %{buildroot}%{_docdir}/%{name}

#gw work around bug #52526
mkdir -p %buildroot%_datadir/%name/help/manual

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
%_datadir/icons/hicolor/*/apps/audacity.*
%_datadir/pixmaps/*
%{_datadir}/mime/packages/audacity.xml
%{_mandir}/man1/audacity.1*



%changelog
* Fri Aug 24 2012 GÃ¶tz Waschk <waschk@mandriva.org> 2.0.2-1mdv2012.0
+ Revision: 815688
- new version

* Thu Jul 19 2012 GÃ¶tz Waschk <waschk@mandriva.org> 2.0.1-1
+ Revision: 810187
- build with ffmpeg 0.7
- replace patch 0 by desktop-file-install
- spec cleanup
- new version

* Fri Mar 16 2012 GÃ¶tz Waschk <waschk@mandriva.org> 2.0.0-1
+ Revision: 785223
- fix file list
- fix linking
- drop patch 1
- update build deps
- new version
- trying to build with new ffmpeg

* Wed Dec 14 2011 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.14-1
+ Revision: 740988
- update build deps
- new version
- rediff patch 8

* Wed Nov 16 2011 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.13-2
+ Revision: 731090
- build with ffmpeg 0.7
- fix for new glib

  + Oden Eriksson <oeriksson@mandriva.com>
    - attempt to relink against libpng15.so.15

* Thu May 05 2011 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.13-1
+ Revision: 669282
- new version
- rediff desktop entry patch
- drop patches 1,11

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.3.12-4
+ Revision: 662888
- mass rebuild

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.12-3mdv2011.0
+ Revision: 603751
- fix build (fix from svn)
- rebuild

* Fri May 07 2010 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.12-2mdv2010.1
+ Revision: 543138
- trying to fix bug #59129, ffmpeg compatibility

* Mon Apr 12 2010 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.12-1mdv2010.1
+ Revision: 533678
- new version
- update file list
- remove old icons

* Tue Jan 19 2010 Frederik Himpe <fhimpe@mandriva.org> 1.3.11-1mdv2010.1
+ Revision: 493817
- Update to new version 1.3.11

* Tue Dec 22 2009 Caio Begotti <caio1982@mandriva.org> 1.3.10-2mdv2010.1
+ Revision: 481346
- small release bump since we now have a newer vamp-plugin-sdk

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - fix soundtouch build dep

* Thu Dec 03 2009 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.10-1mdv2010.1
+ Revision: 472872
- new version
- drop merged patches 12,13,14
- update file list

* Tue Oct 20 2009 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.9-2mdv2010.0
+ Revision: 458411
- fix crash in preferences (bug #54752)

* Tue Sep 01 2009 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.9-1mdv2010.0
+ Revision: 423197
- new version
- add empty help directory (bug #52536)

* Mon Jul 20 2009 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.8-1mdv2010.0
+ Revision: 398063
- fix autotool calls
- new version
- new source URL
- rediff patches 0,6
- drop patches 1,2,4,7,9,11
- fix build with new soundtouch
- update deps

* Mon Mar 30 2009 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.7-5mdv2009.1
+ Revision: 362240
- set alsa as default API

* Sun Mar 29 2009 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.7-4mdv2009.1
+ Revision: 362094
- use the right audio device (bug #49243)
- patch for vamp 1.1 and reenable vamp build
- fix crash in Repeat effect
- make preferences window resizable (bug #49244)

* Sun Mar 08 2009 Frederik Himpe <fhimpe@mandriva.org> 1.3.7-3mdv2009.1
+ Revision: 352938
- Add GTK and X-MandrivaLinux-CrossDesktop menu categories in desktop file
  so that Audacity does not get burried in the More subcategory, because
  Audacity is generally known as the best Linux audio editor, irrespective
  of the used desktop.

* Wed Feb 25 2009 Oden Eriksson <oeriksson@mandriva.com> 1.3.7-2mdv2009.1
+ Revision: 344906
- P10: security fix for CVE-2009-0490 (not needed, but better be safe than sorry)

* Thu Jan 29 2009 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.7-1mdv2009.1
+ Revision: 335054
- new version
- fix format strings
- switch to internal portaudio
- enable jack
- disable vamp plugin support
- copy pulsaudio patch for portaudio

* Sat Dec 13 2008 Adam Williamson <awilliamson@mandriva.org> 1.3.6-2mdv2009.1
+ Revision: 313998
- drop gcc43.patch (was actually merged upstream)
- rediff desktopentry.patch (for fuzz 0)
- drop the pasuspender script - portaudio now works with Pulse, yay

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - suggest optional libs

* Sat Oct 25 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.6-1mdv2009.1
+ Revision: 297174
- enable ffmpeg
- new version
- update build deps
- rediff patch 5

* Mon Jul 28 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.5-3mdv2009.0
+ Revision: 251004
- switch from libresample to libsamplerate to fix bug #42277)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Wed May 21 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.5-2mdv2009.0
+ Revision: 209678
- bump release
- added a gcc43 patch from fedora

* Fri May 09 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.5-1mdv2009.0
+ Revision: 204862
- new version
- drop patches 3,6
- rediff patch 8
- update build deps

* Thu Apr 03 2008 Gustavo De Nardin <gustavodn@mandriva.com> 1.3.4-6mdv2008.1
+ Revision: 192244
- security fix for CVE-2007-6061

* Wed Feb 20 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.4-5mdv2008.1
+ Revision: 173164
- put back translations (bug #37935)

* Fri Feb 15 2008 Frederic Crozat <fcrozat@mandriva.com> 1.3.4-4mdv2008.1
+ Revision: 169023
- Add script to run audacity inside pasuspender if needed

* Wed Feb 13 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.4-3mdv2008.1
+ Revision: 166939
- fix desktop entry (bug #37665)

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 09 2007 Funda Wang <fwang@mandriva.org> 1.3.4-2mdv2008.1
+ Revision: 116690
- drop old menu

* Thu Nov 15 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.4-1mdv2008.1
+ Revision: 108879
- new version
- drop patches 0,1,2,4
- rediff patch 5
- fix buildrequires
- build with wxWidgets 2.8

  + Oden Eriksson <oeriksson@mandriva.com>
    - fix build deps (portaudio-devel)
    - added P3,P4 from debian to make it find the right lame lib
    - added P5 from debian to make it use libresample and optionally libtwolame
      (twolame support is inactive in Mandriva).
    - added P6 from debian to not override CFLAGS
    - added P7 from debian to use external libportaudio
    - generally try to use use external libraries like soundtouch
    - fix build deps

* Fri May 18 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.3-1mdv2008.0
+ Revision: 28074
- fix buildrequires
- new version
- update flac patch
- remove help file


* Tue Dec 12 2006 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.2-4mdv2007.0
+ Revision: 95230
- patch for new libflac

* Mon Nov 06 2006 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.2-3mdv2007.1
+ Revision: 76854
- fix French translation (bug #23469)

* Sun Nov 05 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.3.2-2mdv2007.1
+ Revision: 76690
- patch1: fix soundtouch build on non-x86(-64) archs

* Mon Oct 30 2006 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.2-1mdv2007.1
+ Revision: 73756
- new version
- drop merged patch 1
- drop obsolete source 4
- disable parallel make

* Sat Oct 14 2006 GÃ¶tz Waschk <waschk@mandriva.org> 1.3.0-9mdv2006.0
+ Revision: 64568
- bot-friendly buildrequires
- Import audacity

* Sat Oct 14 2006 Götz Waschk <waschk@mandriva.org> 1.3.0-8mdv2007.1
- unpack patches
- build fix

* Thu Jun 22 2006 Götz Waschk <waschk@mandriva.org> 1.3.0-7mdv2007.0
- fix zh locale
- fix build
- xdg menu

* Fri Apr 28 2006 Götz Waschk <waschk@mandriva.org> 1.3.0-6mdk
- upgrade portaudio to svn snapshot

* Fri Apr 28 2006 Götz Waschk <waschk@mandriva.org> 1.3.0-5mdk
- compile with portaudio v19 (requested by Antoine Pitrou)

* Mon Jan 02 2006 Götz Waschk <waschk@mandriva.org> 1.3.0-4mdk
- fix directory ownership

* Wed Dec 14 2005 Götz Waschk <waschk@mandriva.org> 1.3.0-3mdk
- fix bug 20156 (help file location)

* Thu Dec 01 2005 Götz Waschk <waschk@mandriva.org> 1.3.0-2mdk
- fix desktop entry

* Tue Nov 29 2005 Götz Waschk <waschk@mandriva.org> 1.3.0-1mdk
- register mime types
- update file list
- unicode build
- drop patches
- New release 1.3.0

* Sun Aug 28 2005 Herton Ronaldo Krzesinski <herton@mandriva.com> 1.2.3-4mdk
- rebuild, removed use of %%configure2_5x as something behind it is causing
  audacity after built and installed to segfault while running on a new
  installation or while making access to the "Preferences" window, below is
  the error:

  (audacity:12866): Gtk-CRITICAL **: gtk_accel_label_new: assertion `string != NULL' failed

  (audacity:12866): Gtk-CRITICAL **: gtk_misc_set_alignment: assertion `GTK_IS_MISC (misc)' failed

  (audacity:12866): Gtk-CRITICAL **: gtk_container_add: assertion `GTK_IS_WIDGET (widget)' failed

  (audacity:12866): Gtk-CRITICAL **: gtk_accel_label_set_accel_widget: assertion `GTK_IS_ACCEL_LABEL (accel_label)' failed
  Segmentation fault

* Tue Jun 14 2005 Götz Waschk <waschk@mandriva.org> 1.2.3-3mdk
- work around broken wx-config

* Wed Apr 27 2005 Götz Waschk <waschk@mandriva.org> 1.2.3-2mdk
- rebuild for new wxGTK

* Fri Nov 19 2004 Goetz Waschk <waschk@linux-mandrake.com> 1.2.3-1mdk
- New release 1.2.3

* Thu Nov 11 2004 Götz Waschk <waschk@linux-mandrake.com> 1.2.2-4mdk
- rebuild for new wxGTK

* Tue Oct 12 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.2-3mdk
- C++ fixes
- parallel make now works it seems

* Wed Sep 01 2004 Stew Benedict <sbenedict@mandrakesoft.com> 1.2.2-2mdk
- new icons from André Pascual, Pierre Jarillon (bugzilla #10792)

* Fri Aug 27 2004 Götz Waschk <waschk@linux-mandrake.com> 1.2.2-1mdk
- patch2: fix some missing headers
- drop patch 0
- New release 1.2.2

* Thu Aug 19 2004 Stew Benedict <sbenedict@mandrakesoft.com> 1.2.1-4mdk
- enhanced large icon (Fabien ILLIDE)

* Tue Aug 17 2004 Stew Benedict <sbenedict@mandrakesoft.com> 1.2.1-3mdk
- make icons transparent (bugzilla #10792)

* Tue Jun 08 2004 Götz Waschk <waschk@linux-mandrake.com> 1.2.1-2mdk
- patch for new g++

* Mon May 10 2004 Goetz Waschk <waschk@linux-mandrake.com> 1.2.1-1mdk
- New release 1.2.1

* Thu Apr 29 2004 Götz Waschk <waschk@linux-mandrake.com> 1.2.0-2mdk
- fix build with wxGTK 2.5.1 (pangelo[at]dcc[dot]online.pt)

* Tue Mar 02 2004 Götz Waschk <waschk@linux-mandrake.com> 1.2.0-1mdk
- new version

* Wed Feb 11 2004 Götz Waschk <waschk@linux-mandrake.com> 1.2.0-0.pre4.1mdk
- drop patch 3
- new version

