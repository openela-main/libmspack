Name:           libmspack
Version:        0.7
Release:        0.3.alpha%{?dist}.4
Summary:        Library for CAB and related files compression and decompression

Group:          System Environment/Libraries
License:        LGPLv2
URL:            http://www.cabextract.org.uk/libmspack/
#Source0:        http://www.cabextract.org.uk/libmspack/%{name}-%{version}alpha.tar.gz
Source0:        https://github.com/kyz/libmspack/archive/v0.7alpha/%{name}-v0.7alpha.tar.gz
Patch0:         %{name}-0.4alpha-doc.patch

# Fixes for CVE-2018-18584 CVE-2018-18585
Patch1:         0001-Avoid-returning-CHM-file-entries-that-are-blank-beca.patch
Patch2:         0002-CAB-block-input-buffer-is-one-byte-too-small-for-max.patch
# Fix for CVE-CVE-2019-1010305
Patch3:         0003-length-checks-when-looking-for-control-files.patch

BuildRequires:  doxygen
BuildRequires:  gcc

# Temporarily while building from github tarball:
BuildRequires:  autoconf, automake, libtool


%description
The purpose of libmspack is to provide both compression and decompression of 
some loosely related file formats used by Microsoft.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{name}-doc < 0.2

%description    devel
The %{name}-devel package contains libraries, header files and documentation
for developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}alpha/libmspack
%patch0 -p1
%patch1 -p2
%patch2 -p2
%patch3 -p2

chmod a-x mspack/mspack.h

# Temporarily while building from github tarball:
autoreconf -i


%build
CFLAGS="%{optflags} -fno-strict-aliasing" \
%configure --disable-static --disable-silent-rules

# disable rpath the hard way
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
rm $RPM_BUILD_ROOT%{_libdir}/libmspack.la

iconv -f ISO_8859-1 -t utf8 ChangeLog --output Changelog.utf8
touch -r ChangeLog Changelog.utf8
mv Changelog.utf8 ChangeLog

pushd doc
doxygen
find html -type f | xargs touch -r %{SOURCE0}
rm -f html/installdox
popd

# CVE-2018-18586: The upstream author didn't intend these examples to
# be installed and shipped, and in libmspack 0.9 they are moved into
# an examples directory in the source.  chmextract contains a
# directory traversal exploit.  Remove the binaries.
rm $RPM_BUILD_ROOT%{_bindir}/cabrip
rm $RPM_BUILD_ROOT%{_bindir}/chmextract
rm $RPM_BUILD_ROOT%{_bindir}/msexpand
rm $RPM_BUILD_ROOT%{_bindir}/oabextract


%files
%doc README TODO COPYING.LIB ChangeLog AUTHORS
%{_libdir}/%{name}.so.*

%files devel
%doc doc/html
%{_includedir}/mspack.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Fri Aug  2 2019 Richard W.M. Jones <rjones@redhat.com> - 0.7-0.2.alpha.4
- Fix for CVE-2019-1010305
- Remove "fix" for CVE-2018-14680 as this fix is included in base tar ball.
  resolves: rhbz#1736745, rhbz#1736743

* Thu Mar 21 2019 Richard W.M. Jones <rjones@redhat.com> - 0.7-0.2.alpha.3
- Add gating tests resolves: rhbz#1682770

* Mon Dec 10 2018 Richard W.M. Jones <rjones@redhat.com> - 0.7-0.1.alpha.3
- Fix for CVE-2018-14680
  resolves: rhbz#1610937

* Fri Dec  7 2018 Richard W.M. Jones <rjones@redhat.com> - 0.7-0.1.alpha.2
- Fixes for CVE-2018-18584 CVE-2018-18585.
  resolves: rhbz#1644220

* Wed Nov 14 2018 Richard W.M. Jones <rjones@redhat.com> - 0.7-0.1.alpha.1
- Remove examples (CVE-2018-18586)
  resolves: rhbz#1648376

* Wed Aug 01 2018 Richard W.M. Jones <rjones@redhat.com> - 0.7-0.1.alpha
- New upstream version 0.7alpha.
- No tarball was uploaded so temporarily use tarball from github.
- Fixes CVE-2018-14679 libmspack: off-by-one error in the CHM PMGI/PMGL
  chunk number validity checks

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-0.3.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 19 2017 Dan Horák <dan[at]danny.cz> - 0.6-0.1.alpha
- updated to 0.6alpha (fixes CVE-2017-6419 and CVE-2017-11423)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.10.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.9.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.8.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jul 27 2016 Dan Horák <dan[at]danny.cz> - 0.5-0.7.alpha
- install the actual expand binary

* Wed Jul 27 2016 Dan Horák <dan[at]danny.cz> - 0.5-0.6.alpha
- install the expand tool as msexpand (#1319357)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.5.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 30 2015 Richard W.M. Jones <rjones@redhat.com> - 0.5-0.4.alpha
- Avoid 'test/md5.c:126:3: warning: dereferencing type-punned pointer
  will break strict-aliasing rules' by adding -fno-strict-aliasing flag.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 03 2015 Dan Horák <dan[at]danny.cz> - 0.5-0.1.alpha
- updated to 0.5alpha

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-0.4.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-0.3.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Dan Horák <dan[at]danny.cz> - 0.4-0.1.alpha
- updated to 0.4alpha

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-0.4.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-0.3.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 16 2011 Dan Horák <dan[at]danny.cz> - 0.3-0.1.alpha
- updated to 0.3alpha

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-0.2.20100723alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 30 2010 Dan Horák <dan[at]danny.cz> - 0.2-0.1.20100723alpha
- updated to 0.2alpha released 2010/07/23
- merged the doc subpackage with devel

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.7.20060920alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.6.20060920alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 13 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.5-20060920alpha
- Rebuild for gcc4.3

* Sun Jan 20 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.4.20060920alpha
- installed documentation into html subdir
- manually installed doc's for main package

* Sun Jan 20 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.3.20060920alpha
- Got source using wget -N
- Removed some doc's
- Shifted doc line for doc package
- Added install -p

* Sun Jan 20 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.2.20060920alpha
- Changed install script for doc package
- Fixed rpmlint issue with debug package

* Fri Jan 18 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 20060920cvs.a-1
- Initial release
