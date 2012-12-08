# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 0

%define full_name       jakarta-%{name}
%define section         free

Name:           regexp
Version:        1.5
Release:        %mkrel 0.0.8
Epoch:          0
Summary:        Simple regular expressions API
License:        Apache License
Group:          Development/Java
Url:            http://jakarta.apache.org/%{name}/
Source0:        http://www.apache.org/dist/jakarta/regexp/jakarta-regexp-%{version}.tar.gz
BuildRequires:  java-rpmbuild >= 0:1.6
Requires(pre):     jpackage-utils >= 0:1.6
Requires(postun):  jpackage-utils >= 0:1.6

BuildRequires:  ant >= 1.6
%if ! %{gcj_support}
Buildarch:      noarch
%endif
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
%endif

%description
Regexp is a 100% Pure Java Regular Expression package that was
graciously donated to the Apache Software Foundation by Jonathan Locke.
He originally wrote this software back in 1996 and it has stood up quite
well to the test of time.
It includes complete Javadoc documentation as well as a simple Applet
for visual debugging and testing suite for compatibility.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires(post): %{__rm}
Requires(postun): %{__rm}
Requires(post): /bin/ln

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{full_name}-%{version}
%remove_java_binaries

%build
mkdir lib
export CLASSPATH=
export OPT_JAR_LIST=
%{ant} -Djakarta-site2.dir=. jar javadocs


%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 build/*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -r docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rm -rf docs/api
%{__ln_s} %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# fix end-of-line
for i in `find $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version} -type f -name "*.html" -o -name "*.css"`; do
  %{__perl} -pi -e 's/\r\n/\n/g' $i
done

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}
%endif

%if %{gcj_support}
%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE
%{_javadir}/*.jar
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%dir %{_javadocdir}/%{name}


%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.5-0.0.6mdv2011.0
+ Revision: 669415
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.5-0.0.5mdv2011.0
+ Revision: 607353
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.5-0.0.4mdv2010.1
+ Revision: 523905
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.5-0.0.3mdv2010.0
+ Revision: 426904
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.5-0.0.2mdv2009.1
+ Revision: 351572
- rebuild

* Thu Aug 14 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.5-0.0.1mdv2009.0
+ Revision: 271808
- new version 1.5

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.4-3.0.3mdv2008.1
+ Revision: 121016
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.4-3.0.2mdv2008.0
+ Revision: 87349
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sun Aug 05 2007 David Walluck <walluck@mandriva.org> 0:1.4-3.0.1mdv2008.0
+ Revision: 59200
- sync with JPackage


* Wed Mar 14 2007 Christiaan Welvaart <cjw@daneel.dyndns.org>
+ 2007-03-14 17:48:02 (143747)
- rebuild for 2007.1
- Import regexp

* Tue Jul 25 2006 David Walluck <walluck@mandriva.org> 0:1.4-1.2mdv2007.0
- rebuild

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:1.4-1.1mdv2007.0
- rebuild for libgcj.so.7
- aot-compile

* Sun May 08 2005 David Walluck <david@anti-microsoft.org> 0:1.3-2.1mdk
- release

* Thu Aug 26 2004 Fernando Nasser <fnasser@redhat.com> 0:1.3-2jpp
- Require Ant > 1.6
- Rebuild with Ant 1.6.2

