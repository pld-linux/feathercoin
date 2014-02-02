Summary:	Feathercoin is a peer-to-peer currency
Name:		feathercoin
Version:	0.0.1
Release:	4
License:	MIT/X11
Group:		X11/Applications
Source0:	https://github.com/FeatherCoin/FeatherCoin/archive/master.zip?/%{name}-%{version}.zip
# Source0-md5:	9662befa9e33b7ab7ded60d41cd12eea
URL:		http://www.feathercoin.org
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	boost-devel
BuildRequires:	db-cxx-devel
BuildRequires:	miniupnpc-devel >= 1.5
BuildRequires:	openssl-devel
BuildRequires:	qrencode-devel
BuildRequires:	qt4-qmake
Requires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Feathercoin is a peer-to-peer currency. Peer-to-peer means that no central
authority issues new money or tracks transactions. These tasks are
managed collectively by the network.

%package qt
Summary:	Qt-based Feathercoin Wallet
Group:		X11/Applications

%description qt
Qt-based Feathercoin Wallet.

%prep
%setup -q -c

%build
cd FeatherCoin-master
qmake-qt4 \
	USE_UPNP=1 \
	USE_DBUS=1 \
	USE_QRCODE=1

%{__make}

%{__make} -C src -f makefile.unix \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcflags} %{rpmcxxflags} %{rpmcppflags}"

%install
rm -rf $RPM_BUILD_ROOT
cd FeatherCoin-master

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{_mandir}/man{1,5},%{_localedir},%{_desktopdir},%{_pixmapsdir},%{_datadir}/kde4/services}

install src/feathercoind $RPM_BUILD_ROOT%{_libdir}/%{name}/feathercoind
sed -e 's#/usr/lib/#%{_libdir}/#g' -e 's#bitcoin#feathercoin#g' contrib/debian/bin/bitcoind > $RPM_BUILD_ROOT%{_bindir}/feathercoind
chmod 755 $RPM_BUILD_ROOT%{_bindir}/feathercoind

install feathercoin-qt $RPM_BUILD_ROOT%{_bindir}
sed -e 's#bitcoin#feathercoin#g' contrib/debian/bitcoin-qt.desktop > $RPM_BUILD_ROOT%{_desktopdir}/feathercoin-qt.desktop
sed -e 's#bitcoin#feathercoin#g' contrib/debian/bitcoin-qt.protocol > $RPM_BUILD_ROOT%{_datadir}/kde4/services/feathercoin-qt.protocol

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc FeatherCoin-master/doc/*.txt FeatherCoin-master/contrib/debian/examples/bitcoin.conf
%attr(755,root,root) %{_bindir}/feathercoind
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/feathercoind

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/feathercoin-qt
%{_datadir}/kde4/services/feathercoin-qt.protocol
%{_desktopdir}/feathercoin-qt.desktop
