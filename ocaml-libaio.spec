#  svn checkout  svn://svn.forge.ocamlcore.org/svnroot/libaio-ocaml
#  DATE=$(date +"%Y-%m-%d_%Hh%M")
#  SCM_NAME="libaio-ocaml-$DATE"
#  mv  libaio-ocaml  $SCM_NAME
#  tar cf $SCM_NAME.tar  $SCM_NAME
#  lzma --best  $SCM_NAME.tar

%define base_name       libaio-ocaml
%define arch_version    2009-01-27_10h16
%define pack_version    svn20090127

Name:           ocaml-%{base_name}
Version:        %{pack_version}
Release:	%mkrel 2
Summary:        OCaml bindings for libaio, Linux kernel AIO access library
License:        LGPL
Group:          Development/Other
URL:            https://forge.ocamlcore.org/projects/libaio-ocaml/
Source0:        libaio-ocaml-%{arch_version}.tar.lzma
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib
BuildRequires:  libaio-devel
BuildRequires:  tetex-latex
BuildRequires:  gzip
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
This OCaml-library interfaces the libaio (Linux kernel AIO access
library) C library. It enables ocaml programs to use Linux kernel
fast asynchronous I/O system calls, important for the performance
of databases and other advanced applications.

Compared with the OCaml standard and Unix I/O functions this library:
 * does not block
 * does I/O in the background
 * calls a continuation when the I/O has completed

%package devel
Summary:        OCaml bindings for libaio, Linux kernel AIO access library
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}

%description -n %{name}-devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n libaio-ocaml-%{arch_version}
rm -rf .svn
rm -rf */.svn

%build
make all opt
make doc
gzip --best doc/aio/latex/doc.ps

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_libdir}/ocaml/aio
install -d -m 755 %{buildroot}%{_libdir}/ocaml/stublibs
export DESTDIR=%{buildroot}%{_libdir}/ocaml
#make install
ocamlfind install -destdir $DESTDIR -ldconf /dev/null aio \
    lib/{*.mli,*.cmi,*.cma,*.a,*.cmxa,*.cmx,*.so,META}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE CHANGES README.txt
%dir %{_libdir}/ocaml/aio
%{_libdir}/ocaml/aio/META
%{_libdir}/ocaml/aio/*.cma
%{_libdir}/ocaml/aio/*.cmi
%{_libdir}/ocaml/stublibs/*.so*

%files devel
%defattr(-,root,root)
%doc examples
%doc lib/doc/aio/html
%doc lib/doc/aio/latex/*.{dvi,pdf,ps.gz}
%{_libdir}/ocaml/aio/*.a
%{_libdir}/ocaml/aio/*.ml*
%{_libdir}/ocaml/aio/*.cmx
%{_libdir}/ocaml/aio/*.cmxa

