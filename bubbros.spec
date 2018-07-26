Name:           bubbros
Version:        1.6.2
Release:        6%{?dist}
Summary:        Bub and Brothers game inspired by the classic Bubble and Bobble
Group:          Amusements/Games
License:        MIT and Artistic Licenses
URL:            http://bub-n-bros.sourceforge.net/
Source0:        http://downloads.sourceforge.net/bub-n-bros/%{name}-%{version}.tar.gz
Source1:        bubbros.desktop
Patch0:         bubbros-1.5-fixes.patch
BuildRequires:  python-devel ImageMagick desktop-file-utils libX11-devel
BuildRequires:  libXext-devel xorg-x11-proto-devel java-devel
Requires:       pygame pygtk2 hicolor-icon-theme

%description
This is a direct clone of the MacOS game Bub & Bob of McSebi. Thanks Sebi for
all the cool graphics and sounds!

Features:

    * 1 to 10 players -- the best fun is with at least 3 players!
    * Same gameplay as the famous McSebi's Bub & Bob.
    * Over-the-network game and/or up to 3 players on the same computer.
    * Completely original crazy bonuses!
    * Capture other players in a bubble!
    * New levels, including a random level generator!


%prep
%setup -q
#no backups for this patch, otherwise they end up getting installed!
%patch0 -p1
sed -i 's:#! /usr/bin/env python:#!%{__python}:' BubBob.py bubbob/bb.py \
  display/Client.py
chmod +x display/Client.py
# for %doc
mv bubbob/levels/README.txt levels.txt


%build
make %{?_smp_mflags}
pushd bubbob/images
python buildcolors.py
popd
pushd java
rm *.class
make
popd
convert bubbob/images/dragon_0.ppm -transparent '#010101' -crop 32x32+0+0 \
  %{name}.png


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man6
# copying the complete dirs and then removing the unwanted bits is easier :)
cp -a BubBob.py bubbob common display http2 java metaserver \
  $RPM_BUILD_ROOT%{_datadir}/%{name}
rm -fr $RPM_BUILD_ROOT%{_datadir}/%{name}/bubbob/build
rm -fr $RPM_BUILD_ROOT%{_datadir}/%{name}/bubbob/doc
rm -fr $RPM_BUILD_ROOT%{_datadir}/%{name}/display/build
rm -fr $RPM_BUILD_ROOT%{_datadir}/%{name}/display/windows
rm     $RPM_BUILD_ROOT%{_datadir}/%{name}/display/*_windows.py
rm -fr $RPM_BUILD_ROOT%{_datadir}/%{name}/http2/sf
rm     $RPM_BUILD_ROOT%{_datadir}/%{name}/http2/header.png
rm     $RPM_BUILD_ROOT%{_datadir}/%{name}/java/pclient.java
rm `find $RPM_BUILD_ROOT%{_datadir}/%{name} -name '*.c'`
rm `find $RPM_BUILD_ROOT%{_datadir}/%{name} -name 'Makefile'`
rm `find $RPM_BUILD_ROOT%{_datadir}/%{name} -name 'setup.py'`
# put the .so files in %{libdir}
mv `find $RPM_BUILD_ROOT%{_datadir}/%{name} -name '*.so'` \
  $RPM_BUILD_ROOT%{_libdir}/%{name}
# create the symlinks in /usr/bin, these must be absolute links!
ln -s %{_datadir}/%{name}/BubBob.py $RPM_BUILD_ROOT%{_bindir}/bubbros
ln -s %{_datadir}/%{name}/bubbob/bb.py $RPM_BUILD_ROOT%{_bindir}/bubbros-server
ln -s %{_datadir}/%{name}/display/Client.py \
  $RPM_BUILD_ROOT%{_bindir}/bubbros-client
# install the manpages
install -m 644 doc/BubBob.py.1 $RPM_BUILD_ROOT%{_mandir}/man6/bubbros.6
install -m 644 doc/bb.py.1 $RPM_BUILD_ROOT%{_mandir}/man6/bubbros-server.6
install -m 644 doc/Client.py.1 $RPM_BUILD_ROOT%{_mandir}/man6/bubbros-client.6
# below is the desktop file and icon stuff.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install \
%if 0%{?fedora} && 0%{?fedora} < 19
  --vendor dribble \
%endif
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
install -p -m 644 %{name}.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc LICENSE.txt artistic.txt levels.txt
%{_bindir}/bubbros*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_mandir}/man6/bubbros*.6.gz


%changelog
* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 28 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 18 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Oct 13 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.6.2-1
- New upstream release 1.6.2

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.6-8
- Mass rebuilt for Fedora 19 Features

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 25 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 1.6-6
- Rebuild for new python

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.6-5
- rebuild for new F11 features

* Wed Dec 17 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.6-4
- Drop no longer needed htmlview requires

* Wed Dec 17 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.6-3
- Rebuild for new python

* Thu Jul 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.6-2
- Release bump for rpmfusion

* Mon Sep 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.6-1
- New upstream release 1.6

* Mon Jan 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.5-3
- Rebuild (with compile and run fixes) for new python2.5

* Tue Aug  1 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.5-2
- Add missing BuildRequires: libX11-devel libXext-devel xorg-x11-proto-devel
- Add Requires: htmlview
- Recompile java code instead of using precompiled .class files
- Don't install java source code, only class files

* Fri Jul 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.5-1
- initial Dribble package
