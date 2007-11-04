Summary:	A program to rename and rotate files according to EXIF tags
Summary(pl.UTF-8):	Program do zmiany nazwy i obrotu plików wykorzystując dane EXIF.
Name:		renrot
Version:	0.25
Release:	0.2
License:	GPL or Artistic
Group:		Applications/Multimedia
URL:		http://freshmeat.net/projects/renrot/
Source0:	ftp://ftp.dn.farlep.net/pub/misc/renrot/%{name}-%{version}.tar.gz
BuildRequires:	perl(Getopt::Long) >= 2.34
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-Image-ExifTool >= 5.72
Requires:	libjpeg >= 6b
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Renrot renames files according the DateTimeOriginal and FileModifyDate
EXIF tags, if they exist. Otherwise, the name will be set according to
the current timestamp. Additionally, it rotates files and their
thumbnails, accordingly Orientation EXIF tag.

The script can also put commentary into the Commentary and UserComment
tags.

Personal details can be specified via XMP tags defined in a
configuration file.

%description -l pl.UTF8
Renrot zamienia pliki na podstawie tagów EXIF: DateTimeOriginal i
FileModifyDate w przypadku gdy one istnieją. W innych przypadkach,
nazwa będzie zmieniona nawiązując do znacznika czasu. Dodatkowo
obraca pliki i ich miniaturki odpowiednio do tagu EXIF: "Ułożenie".

%prep
%setup -q

%build
%{__perl} Makefile.PL PREFIX=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install PREFIX=$RPM_BUILD_ROOT%{_prefix}

# Fix renrot permissions
chmod 755 $RPM_BUILD_ROOT%{_bindir}/renrot

# install sample confuration files
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install etc/colors.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install etc/copyright.tag $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install etc/renrot.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install etc/tags.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

# Remove some unwanted files
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name perllocal.pod -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- renrot < 0.21-0.2.rc2
if [ -f %{_sysconfdir}/renrot.rc ]; then
    /bin/mkdir -p %{_sysconfdir}/%{name}
    /bin/mv -fb %{_sysconfdir}/renrot.rc %{_sysconfdir}/%{name}/renrot.conf
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README ChangeLog NEWS TODO
%lang(ru) %doc README.russian
%attr(755,root,root) %{_bindir}/renrot
#%{_mandir}/man1/*.1*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/colors.conf
%config(noreplace) %{_sysconfdir}/%{name}/copyright.tag
%config(noreplace) %{_sysconfdir}/%{name}/renrot.conf
%config(noreplace) %{_sysconfdir}/%{name}/tags.conf
