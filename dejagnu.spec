Summary: A front end for testing other programs
Name: dejagnu
Version: 1.4.4
Release: 17%{?dist}
Epoch: 1
License: GPLv2+
Source: ftp://ftp.gnu.org/gnu/dejagnu/dejagnu-%{version}.tar.gz
Source2: dejagnu.texi
Group: Development/Tools
URL: http://www.gnu.org/software/dejagnu/
Requires: expect
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: expect screen texinfo
Patch1: dejagnu-1.4.4-smp-1.patch
Patch3: dejagnu-1.4.4-testsuite.patch
Patch4: dejagnu-1.4.4-runtest.patch
Patch5: dejagnu-1.4.4-utils-speedup.patch

%description
DejaGnu is an Expect/Tcl based framework for testing other programs.
DejaGnu has several purposes: to make it easy to write tests for any
program; to allow you to write tests which will be portable to any
host or target where a program must be tested; and to standardize the
output format of all tests (making it easier to integrate the testing
into software development).

%prep
%setup -q
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%configure -v
makeinfo %{SOURCE2} -o doc/%{name}.info

%check
echo ============TESTING===============
# Dejagnu test suite also has to test reporting to user.  It needs a
# terminal for that.  That doesn't compute in mock.  Work around it by
# running the test under screen and communicating back to test runner
# via temporary file.  If you have better idea, we accept patches.
TMP=`mktemp`
screen -D -m sh -c '(make check RUNTESTFLAGS="RUNTEST=`pwd`/runtest"; echo $?) >> '$TMP
RESULT=`tail -n 1 $TMP`
cat $TMP
rm -f $TMP
echo ============END TESTING===========
exit $RESULT

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
chmod a-x $RPM_BUILD_ROOT/%{_datadir}/dejagnu/runtest.exp
make -C doc DESTDIR=$RPM_BUILD_ROOT install-man
install -D -m 644 doc/dejagnu.info $RPM_BUILD_ROOT/%{_infodir}/%{name}.info

%post
/sbin/install-info %{_infodir}/%{name}.info.gz --dir-file=%{_infodir}/dir &> /dev/null
:

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir &> /dev/null
fi
:

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING NEWS README AUTHORS ChangeLog doc/overview.pdf
%{_bindir}/runtest
%{_datadir}/dejagnu
%{_includedir}/dejagnu.h
%{_mandir}/*/*
%{_infodir}/*

%changelog
* Fri Jan 22 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 1.4.4-17
- added utils speedup patch from jakub@redhat.com
- Resolves: #557564

* Fri Oct 16 2009 Jiri Moskovcak <jmoskovc@redhat.com> - 1.4.4-16
- fixed installation with --excludedocs rhbz#515949

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 27 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 1:1.4.4-13
- rewriten patch to work with fuzz=0

* Wed Aug 27 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 1:1.4.4-12
- fixed runtest (patch from jan.kratochvil@redhat.com)
- Resolves: #460153

* Mon Nov 12 2007 Petr Machata <pmachata@redhat.com> - 1:1.4.4-11
- Install info file.
- Resolves: #230652

* Thu Oct  4 2007 Petr Machata <pmachata@redhat.com> - 1:1.4.4-10
- A few more cleanups after discussion with reviewer.
- Resolves: #225679

* Wed Oct  3 2007 Petr Machata <pmachata@redhat.com> - 1:1.4.4-9
- Clean up spec per merge review comments.
- Fix testsuite.
- Resolves: #225679

* Thu Aug 16 2007 Petr Machata <pmachata@redhat.com> - 1:1.4.4-8
- Fix licesing tag.

* Wed Mar  7 2007 Petr Machata <pmachata@redhat.com> - 1:1.4.4-7
- Remove mention of dejagnu.info from manpage, per comments in
  doc/Makefile.
- Resolves: #230652

* Wed Feb  7 2007 Petr Machata <pmachata@redhat.com> - 1:1.4.4-6
- Tidy up the specfile per rpmlint comments

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.4.4-5.1
- rebuild

* Wed Feb 2 2006 Petr Machata <pmachata@redhat.com> 1:1.4.4-5
- Applying H.J. Lu's race condition patch. (#166000)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Mar  5 2005 Jakub Jelinek <jakub@redhat.com> 1:1.4.4-4
- rebuilt with GCC 4

* Mon Nov  8 2004 Jakub Jelinek <jakub@redhat.com> 1:1.4.4-3
- add URL (#138280)

* Mon Sep 27 2004 Warren Togami <wtogami@redhat.com> 1:1.4.4-2
- remove INSTALL & redundant copies of overview

* Tue Aug  3 2004 Jakub Jelinek <jakub@redhat.com> 1:1.4.4-1
- update to 1.4.4
- run make check during rpm build

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec 30 2002 Karsten Hopp <karsten@redhat.de> 1:1.4.2-9
- more missing BuildRequires

* Tue Dec 17 2002 Karsten Hopp <karsten@redhat.de> 1:1.4.2-8
- Add jadetex Buildrequires

* Wed Nov 27 2002 Tim Powers <timp@redhat.com> 1:1.4.2-7
- include dejagnu.h
- move %%{_libexecdir}/config.guess into %%{_datadir}/dejagnu 
- include overview docs (bug #59095)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 29 2002 Jakub Jelinek <jakub@redhat.com> 1.4.2-4
- fix makefile style variable passing (#63984)

* Thu Feb 28 2002 Jakub Jelinek <jakub@redhat.com> 1.4.2-3
- rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Nov 28 2001 Jakub Jelinek <jakub@redhat.com> 1.4.2-1
- update to 1.4.2, mainly so that it can be built with gcc3+

* Fri Sep  7 2001 Jakub Jelinek <jakub@redhat.com> 1.4.1-3
- make it noarch again

* Wed Aug 29 2001 Jakub Jelinek <jakub@redhat.com>
- fix a typo (#52404)

* Thu Jun 28 2001 Tim Powers <timp@redhat.com>
- rebuilt for the distro

* Tue Feb 27 2001 Tim Powers <timp@redhat.com>
- minor modifications to the spec file. Built for Powertools.
- added Epoch

* Wed Feb 21 2001 Rob Savoye <rob@welcomehome.org>
- Fixed Requires line, and changed the URL to the new ftp site.

* Sun Oct 31 1999 Rob Savoye <rob@welcomehome.org>
- updated to the latest snapshot
- added doc files
- added the site.exp config file

* Mon Jul 12 1999 Tim Powers <timp@redhat.com>
- updated to 19990628
- updated patches as needed
- added %%defattr in files section

* Wed Mar 10 1999 Jeff Johnson <jbj@redhat.com>
- add alpha expect patch (#989)
- use %%configure

* Thu Dec 17 1998 Jeff Johnson <jbj@redhat.com>
- Update to 19981215.

* Thu Nov 12 1998 Jeff Johnson <jbj@redhat.com>
- Update to 1998-10-29.

* Wed Jul  8 1998 Jeff Johnson <jbj@redhat.com>
- Update to 1998-05-28.

* Sun Feb  1 1998 Jeff Johnson <jbj@jbj.org>
- Create.
 
