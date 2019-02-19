%{?_javapackages_macros:%_javapackages_macros}

%global full_name       jakarta-%{name}

Name:           regexp
Version:        1.5
Release:        19
Summary:        Simple regular expressions API
Group:          Development/Java
License:        ASL 2.0

Url:            http://jakarta.apache.org/%{name}/
Source0:        http://www.apache.org/dist/jakarta/regexp/jakarta-regexp-%{version}.tar.gz
Source1:        http://repo.maven.apache.org/maven2/%{full_name}/%{full_name}/1.4/%{full_name}-1.4.pom
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  java-devel
Requires:       java

BuildRequires:  ant >= 1.6
BuildArch:      noarch

%description
Regexp is a 100% Pure Java Regular Expression package that was
graciously donated to the Apache Software Foundation by Jonathan Locke.
He originally wrote this software back in 1996 and it has stood up quite
well to the test of time.
It includes complete Javadoc documentation as well as a simple Applet
for visual debugging and testing suite for compatibility.

%package javadoc

Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{full_name}-%{version}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%build
mkdir lib
ant -Djakarta-site2.dir=. jar javadocs


%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 build/*.jar %{buildroot}%{_javadir}/%{name}.jar

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr docs/api/* %{buildroot}%{_javadocdir}/%{name}

%check
ant -Djakarta-site2.dir=. test

%files
%doc LICENSE
%{_javadir}/%{name}.jar

%files javadoc
%doc LICENSE
%{_javadocdir}/%{name}
