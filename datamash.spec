# Location for bash completions.  define, not global, is for lazy expansion.
# On el6, which doesn't have pkg-config for bash-completion,
# /etc/bash_completion.d seems to be the correct location, with a
# lot of entries symlinked from /usr/share/bash-completion.
%define compdir %(pkg-config --exists bash-completion &&
		     pkg-config --variable=completionsdir bash-completion ||
		     echo %_sysconfdir/bash_completion.d)

Name:           datamash
Version:        1.2
Release:        1%{?dist}
Summary:        A statistical, numerical and textual operations tool

License:        GPLv3+
URL:            https://www.gnu.org/software/%{name}/
Source0:        http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

Provides:       bundled(gnulib)
BuildRequires:  gettext perl(Digest::MD5) perl(Digest::SHA) perl(Data::Dumper)
BuildRequires:  pkgconfig bash-completion
Requires(preun): info
Requires(post): info

%description
GNU datamash is a command-line program which performs basic
numeric,textual and statistical operations on input textual data
files.

%prep
%autosetup
# .UR not defined in el6 an macros
%{?el6:sed -i -e 's/^.UR //g' datamash.1}

%build
%configure
%make_build

%install
%{__rm} -rf %{buildroot}
%make_install
%{__rm} -f %{buildroot}/%{_infodir}/dir
%find_lang %{name}
%{__mkdir_p} %{buildroot}%{compdir}
%{__mv} %{buildroot}%{_datadir}/datamash/bash-completion.d/datamash %{buildroot}%{compdir}
# rpmlint: E: sourced-script-with-shebang /etc/bash_completion.d/datamash /bin/bash
%{__sed} -i '1d' %{buildroot}%{compdir}/datamash

%check
%{__make} check


%files -f %{name}.lang
%{_bindir}/datamash
%{_datadir}/datamash/
%{_infodir}/datamash.info.gz
%dir %{compdir}/..
%dir %{compdir}
%{compdir}/datamash

%license COPYING
%doc README-release README NEWS THANKS TODO AUTHORS ChangeLog
%{_mandir}/man1/datamash.1.gz

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%changelog
* Tue Sep 05 2017 Hannes Frederic Sowa <hannes@stressinduktion.org> - 1.2-1
- new upstream release 1.2-1

* Fri Jun 30 2017 Hannes Frederic Sowa <hannes@stressinduktion.org> 1.1.1-1
- Initial version of the package
