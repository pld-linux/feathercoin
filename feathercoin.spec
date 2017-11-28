# NOTE: "portable wallet" wants BDB 4.8
#
# Conditional build:
%bcond_with	ccache	# use ccache for building
%bcond_without	gui	# Qt5 GUI

Summary:	Feathercoin - a peer-to-peer currency
Summary(pl.UTF-8):	Feathercoin - waluta peer-to-peer
Name:		feathercoin
Version:	0.9.6
Release:	3
License:	MIT
Group:		Applications/Networking
#Source0Download: https://github.com/FeatherCoin/Feathercoin/releases
Source0:	https://github.com/FeatherCoin/Feathercoin/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9ac8509ab7bc7fb39b8e9d474a1079e3
Patch0:		%{name}-c++.patch
Patch1:		%{name}-zxing.patch
Patch2:		x32.patch
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
BuildRequires:	boost-devel
%{?with_ccache:BuildRequires:	ccache}
BuildRequires:	db-cxx-devel >= 4.8
BuildRequires:	gettext-tools
%{?with_gui:BuildRequires:	libpng-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	miniupnpc-devel >= 1.5
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	protobuf-devel
BuildRequires:	qrencode-devel
%{?with_gui:BuildRequires:	qt5-build >= 5}
BuildRequires:	zxing-cpp-devel
%{?with_gui:BuildRequires:	zlib-devel}
Requires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Feathercoin is a peer-to-peer currency. Peer-to-peer means that no
central authority issues new money or tracks transactions. These tasks
are managed collectively by the network.

%description -l pl.UTF-8
Feathercoin to waluta peer-to-peer. Peer-to-peer oznacza, że nie ma
centralnego urzędu, który emituje nowe pieniądze czy śledzi
transakcje. Zadania te są obsługiwane zespołowo przez sieć.

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
%ifarch x32
%patch2 -p1
%endif

%build
install -d src/build-aux
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
# --with-gui defaults to qt4, but it doesn't build (QJsonObject is required)
%configure \
	--enable-ccache%{!?with_ccache:=no} \
	--disable-silent-rules \
	--with-incompatible-bdb \
	--with-gui=%{?with_gui:qt5}%{!?with_gui:no}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_mandir}/man{1,5},%{_desktopdir},%{_datadir}/kde4/services}
sed -e 's#bitcoin#feathercoin#g;s#Bitcoin#Feathercoin#g' contrib/debian/bitcoin-qt.desktop > $RPM_BUILD_ROOT%{_desktopdir}/feathercoin-qt.desktop
sed -e 's#bitcoin#feathercoin#g' contrib/debian/bitcoin-qt.protocol > $RPM_BUILD_ROOT%{_datadir}/kde4/services/feathercoin-qt.protocol
cp -p contrib/debian/manpages/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p contrib/debian/manpages/*.5 $RPM_BUILD_ROOT%{_mandir}/man5

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.md doc/*.txt contrib/debian/examples/bitcoin.conf
%attr(755,root,root) %{_bindir}/feathercoin-cli
%attr(755,root,root) %{_bindir}/feathercoind
%attr(755,root,root) %{_bindir}/test_bitcoin
%{_mandir}/man1/feathercoin-cli.1*
%{_mandir}/man1/feathercoind.1*
%{_mandir}/man5/feathercoin.conf.5*

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/feathercoin-qt
%attr(755,root,root) %{_bindir}/test_bitcoin-qt
%{_datadir}/kde4/services/feathercoin-qt.protocol
%{_desktopdir}/feathercoin-qt.desktop
%{_mandir}/man1/feathercoin-qt.1*
