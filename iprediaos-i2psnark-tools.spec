Name:		iprediaos-i2psnark-tools
Version:	0.0.1
Release:	1%{?dist}
Summary:	IprediaOS I2PSnark configuration and tools

Group:		Applications/Internet
License:	GPL
URL:		http://www.ipredia.org
Source0:	%{name}-%{version}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

Requires:	i2p

%description
Configuration and tools for I2PSnark.

%prep
%setup -q


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%post
# Create a shared folder
install -d /home/shares
# Create a folder for downloads
install -d /home/shares/Downloads
/usr/bin/setfacl -R -m u::rwx,g::rwx,o::rwx /home/shares/Downloads
/usr/bin/setfacl -R -d -m u::rwx,g::rwx,o::rwx /home/shares/Downloads
# Change i2psnark download folder (installation folder and configuration folder)
sed -i 's:i2psnark.dir=i2psnark:i2psnark.dir=/home/shares/Downloads:g' /usr/bin/i2p/i2psnark.config
if [ -a "/usr/local/i2p/.i2p/i2psnark.config" ]; then
	sed -i 's:i2psnark.dir=i2psnark:i2psnark.dir=/home/shares/Downloads:g' /usr/local/i2p/.i2p/i2psnark.config
fi

# Reload configuration
service i2p condrestart > /dev/null 2>&1
/usr/bin/update-desktop-database &> /dev/null || :
exit 0


%postun
/usr/bin/update-desktop-database &> /dev/null || :


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
%{_datadir}/applications/i2psnark.desktop


%changelog
* Mon Mar 5 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.0.1-1
- Initial package
