Summary: Experimental HTTP/2 client, server and proxy
Name: nghttp2
Version: 1.41.0
Release: 1
License: MIT
URL: https://nghttp2.org/
Source0:    %{name}-%{version}.tar.bz2

BuildRequires: gcc-c++
BuildRequires: libev-devel
BuildRequires: pkgconfig(libcares)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(python3)
BuildRequires: pkgconfig(zlib)

Requires: libnghttp2 = %{version}-%{release}

%description
This package contains the HTTP/2 client, server and proxy programs.


%package -n libnghttp2
Summary: A library implementing the HTTP/2 protocol

%description -n libnghttp2
libnghttp2 is a library implementing the Hypertext Transfer Protocol
version 2 (HTTP/2) protocol in C.


%package -n libnghttp2-devel
Summary: Files needed for building applications with libnghttp2
Requires: libnghttp2 = %{version}-%{release}
Requires: pkgconfig

%description -n libnghttp2-devel
The libnghttp2-devel package includes libraries and header files needed
for building applications with libnghttp2.

%package doc
Summary: Documentation for nghttp2
BuildArch: noarch

%description doc
This package contains the documentation for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

# make fetch-ocsp-response use Python 3
sed -e '1 s|^#!/.*python|&3|' -i script/fetch-ocsp-response

%build
autoreconf --force --install
# From configure: enable-lib-only is a short hand for --disable-app --disable-examples
# --disable-hpack-tools --disable-python-bindings
%configure PYTHON=%{__python3}              \
    --disable-static                        \
    --enable-lib-only                       \
    --with-libxml2                          \
    --without-spdylay

# avoid using rpath
sed -i libtool                              \
    -e 's/^runpath_var=.*/runpath_var=/'    \
    -e 's/^hardcode_libdir_flag_spec=".*"$/hardcode_libdir_flag_spec=""/'

%make_build V=1


%install
%make_install
# not needed on SailfishOS
rm -f "$RPM_BUILD_ROOT%{_libdir}/libnghttp2.la"

# will be installed via %%doc
rm -f "$RPM_BUILD_ROOT%{_datadir}/doc/nghttp2/README.rst"

# Drop as we don't servers
rm -f "$RPM_BUILD_ROOT%{_datadir}/nghttp2/fetch-ocsp-response"

%post -p /sbin/ldconfig -n libnghttp2
%postun -p /sbin/ldconfig -n libnghttp2

%check
# test the just built library instead of the system one, without using rpath
export "LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}:$LD_LIBRARY_PATH"
make check

%files -n libnghttp2
%{_libdir}/libnghttp2.so.*
%license COPYING

%files -n libnghttp2-devel
%{_includedir}/nghttp2
%{_libdir}/pkgconfig/libnghttp2.pc
%{_libdir}/libnghttp2.so

%files doc
%license COPYING
%doc README.rst
%{_mandir}/man1/h2load.1*
%{_mandir}/man1/nghttp.1*
%{_mandir}/man1/nghttpd.1*
%{_mandir}/man1/nghttpx.1*
