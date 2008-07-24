Name:           bubbros
Version:        1.6
Release:        2%{?dist}
Summary:        Bub and Brothers game inspired by the classic Bubble and Bobble
Group:          Amusements/Games
License:        MIT and Artistic Licenses
URL:            http://bub-n-bros.sourceforge.net/
Source0:        http://downloads.sourceforge.net/bub-n-bros/%{name}-%{version}.tar.bz2
Source1:        bubbros.desktop
Patch0:         bubbros-1.5-fixes.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python-devel ImageMagick desktop-file-utils libX11-devel
BuildRequires:  libXext-devel xorg-x11-proto-devel java-1.4.2-gcj-compat-devel
Requires:       pygame pygtk2 htmlview hicolor-icon-theme

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
rm -rf $RPM_BUILD_ROOT
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
desktop-file-install --vendor dribble           \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
install -p -m 644 %{name}.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%doc LICENSE.txt artistic.txt levels.txt
%{_bindir}/bubbros*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_mandir}/man6/bubbros*.6.gz


%changelog
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
