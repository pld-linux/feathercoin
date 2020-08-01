# NOTE: "portable wallet" wants BDB 4.8
#
# Conditional build:
%bcond_with	ccache	# use ccache for building
%bcond_without	gui	# Qt5 GUI

Summary:	Feathercoin - a peer-to-peer currency
Summary(pl.UTF-8):	Feathercoin - waluta peer-to-peer
Name:		feathercoin
Version:	0.18.3
Release:	3
License:	MIT
Group:		Applications/Networking
#Source0Download: https://github.com/FeatherCoin/Feathercoin/releases
Source0:	https://github.com/FeatherCoin/Feathercoin/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e5e3fc683a09ec7c2efc21dda691c402
Patch0:		lib.patch
Patch1:		qt-5.15.patch
Patch2:		%{name}-includes.patch
URL:		https://www.feathercoin.com/
%if %{with gui}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5DBus-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Network-devel >= 5
BuildRequires:	Qt5PrintSupport-devel >= 5
BuildRequires:	Qt5Test-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
%endif
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.47.0
%{?with_ccache:BuildRequires:	ccache}
BuildRequires:	db-cxx-devel >= 4.8
BuildRequires:	gettext-tools
%{?with_gui:BuildRequires:	libpng-devel}
BuildRequires:	libsecp256k1-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libunivalue-devel >= 1.0.4
BuildRequires:	miniupnpc-devel >= 1.5
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	protobuf-devel
BuildRequires:	qrencode-devel
%{?with_gui:BuildRequires:	qt5-build >= 5}
BuildRequires:	zeromq-devel >= 4
%{?with_gui:BuildRequires:	zlib-devel}
BuildRequires:	zxing-cpp-devel
Requires:	libunivalue >= 1.0.4
Requires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# uses nNeoScryptOptions symbol from binaries
%define		skip_post_check_so	libbitcoinconsensus.so.*

%description
Feathercoin is a peer-to-peer currency. Peer-to-peer means that no
central authority issues new money or tracks transactions. These tasks
are managed collectively by the network.

%description -l pl.UTF-8
Feathercoin to waluta peer-to-peer. Peer-to-peer oznacza, że nie ma
centralnego urzędu, który emituje nowe pieniądze czy śledzi
transakcje. Zadania te są obsługiwane zespołowo przez sieć.

%package devel
Summary:	Header file for bitcoinconsensus library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki bitcoinconsensus
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel
Conflicts:	bitcoin-devel

%description devel
Header file for bitcoinconsensus library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki bitcoinconsensus.

%package static
Summary:	Static bitcoinconsensus library
Summary(pl.UTF-8):	Statyczna biblioteka bitcoinconsensus
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Conflicts:	bitcoin-static

%description static
Static bitcoinconsensus library.

%description static -l pl.UTF-8
Statyczna biblioteka bitcoinconsensus.

%package qt
Summary:	Qt-based Feathercoin Wallet
Summary(pl.UTF-8):	Oparty na Qt portfel Feathercoin
Group:		X11/Applications

%description qt
Qt-based Feathercoin Wallet.

%description qt -l pl.UTF-8
Oparty na Qt portfel Feathercoin.

%prep
%setup -q -n Feathercoin-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# --with-gui defaults to qt4, but it doesn't build (QJsonObject is required)
%configure \
	--enable-ccache%{!?with_ccache:=no} \
	--disable-silent-rules \
	--with-gui=%{?with_gui:qt5}%{!?with_gui:no} \
	--with-incompatible-bdb \
	--with-system-univalue

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbitcoinconsensus.la

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_datadir}/kde4/services}
cat <<EOF >$RPM_BUILD_ROOT%{_desktopdir}/feathercoin-qt.desktop
[Desktop Entry]
Encoding=UTF-8
Name=Feathercoin
Comment=Feathercoin P2P Cryptocurrency
Comment[fr]=Feathercoin, monnaie virtuelle cryptographique pair à pair
Comment[pl]=Feathercoin - kryptowaluta P2P
Comment[tr]=Feathercoin, eşten eşe kriptografik sanal para birimi
Exec=feathercoin-qt %u
Terminal=false
Type=Application
Icon=bitcoin128
MimeType=x-scheme-handler/feathercoin;
Categories=Office;Finance;
EOF

cat <<EOF >$RPM_BUILD_ROOT%{_datadir}/kde4/services/feathercoin-qt.protocol
[Protocol]
exec=feathercoin-qt '%u'
protocol=feathercoin
input=none
output=none
helper=true
listing=
reading=false
writing=false
makedir=false
deleting=false
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md doc/*.txt
%attr(755,root,root) %{_bindir}/feathercoin-cli
%attr(755,root,root) %{_bindir}/feathercoin-tx
%attr(755,root,root) %{_bindir}/feathercoin-wallet
%attr(755,root,root) %{_bindir}/feathercoind
%{_mandir}/man1/feathercoin-cli.1*
%{_mandir}/man1/feathercoin-tx.1*
%{_mandir}/man1/feathercoin-wallet.1*
%{_mandir}/man1/feathercoind.1*
%attr(755,root,root) %{_libdir}/libbitcoinconsensus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbitcoinconsensus.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbitcoinconsensus.so
%{_includedir}/bitcoinconsensus.h
%{_pkgconfigdir}/libbitcoinconsensus.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libbitcoinconsensus.a

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/feathercoin-qt
%{_datadir}/kde4/services/feathercoin-qt.protocol
%{_desktopdir}/feathercoin-qt.desktop
%{_mandir}/man1/feathercoin-qt.1*
