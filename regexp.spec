%define full_name	jakarta-%{name}
%define section		free
%define gcj_support	1

Name:           regexp
Version:        1.4
Release:        %mkrel 1.3
Epoch:          0
Summary:        Simple regular expressions API
License:        Apache License
Group:          Development/Java
#Distribution:   JPackage
#Vendor:         JPackage Project
Url:            http://jakarta.apache.org/%{name}/
Source0:        http://www.apache.org/dist/jakarta/regexp/jakarta-regexp-%{version}.tar.bz2
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  ant >= 0:1.6
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
Buildroot:      %{_tmppath}/%{name}-%{version}-buildroot
# RHEL3 and FC2
#Obsoletes:      %{full_name} <= 0:1.2

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

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{full_name}-%{version}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%build
mkdir lib
%ant -Djakarta-site2.dir=. jar javadocs


%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 build/*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -r docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rm -rf docs/api

# fix end-of-line
for i in `find $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version} -type f -name "*.html" -o -name "*.css"`; do
  %{__perl} -pi -e 's/\r\n/\n/g' $i
done

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc README LICENSE
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

