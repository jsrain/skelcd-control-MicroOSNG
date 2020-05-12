#
# spec file for package skelcd-control-MicroOSNG
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

######################################################################
#
# IMPORTANT: Please do not change the control file or this spec file
#   in build service directly, use
#   https://github.com/yast/skelcd-control-MicroOSNG repository
#
#   See https://github.com/yast/skelcd-control-MicroOSNG/blob/master/CONTRIBUTING.md
#   for more details.
#
######################################################################

Name:           skelcd-control-MicroOSNG
# xmllint
BuildRequires:  libxml2-tools
# xsltproc
BuildRequires:  libxslt-tools
# RNG schema
BuildRequires:  yast2-installation-control

######################################################################
#
# Here is the list of Yast packages which are needed in the
# installation system (inst-sys) for the Yast installer
#

# branding
# FIXME Requires:       yast2-qt-branding-SLE
Requires:       yast2-theme

# Generic Yast packages needed for the installer
Requires:       autoyast2
Requires:       yast2-add-on
Requires:       yast2-buildtools
Requires:       yast2-caasp >= 4.2.1
Requires:       yast2-devtools
Requires:       yast2-fcoe-client
# For creating the AutoYast profile at the end of installation (bnc#887406)
Requires:       yast2-firewall
# instsys_cleanup
Requires:       yast2-installation >= 3.1.217.9
Requires:       yast2-iscsi-client
Requires:       yast2-kdump
Requires:       yast2-multipath
Requires:       yast2-network >= 3.1.42
Requires:       yast2-nfs-client
Requires:       yast2-ntp-client
Requires:       yast2-proxy
Requires:       yast2-services-manager
Requires:       yast2-slp
Requires:       yast2-trans-stats
Requires:       yast2-tune
Requires:       yast2-update
Requires:       yast2-users
Requires:       yast2-x11
# Ruby debugger in the inst-sys (FATE#318421)
Requires:       rubygem(%{rb_default_ruby_abi}:byebug)
# Install and enable xrdp by default (FATE#320363)
Requires:       yast2-rdp

# Ensure no two skelcd-control-* packages can be installed in the same time,
# an OBS check reports a file conflict for the /CD1/control.xml file from
# the other packages.
Conflicts:      product_control
Provides:       product_control
Provides:       system-installation() = MicroOSNG

# Architecture specific packages
#

%ifarch %ix86 x86_64
Requires:  yast2-vm
%endif

#
######################################################################

Url:            https://github.com/yast/skelcd-control-MicroOSNG
AutoReqProv:    off
Version:        1.0.0
Release:        0
Summary:        The MicroOSNG Installation Control file
License:        MIT
Group:          Metapackages
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source:         skelcd-control-MicroOSNG-%version.tar.bz2
Provides:       product_control
Conflicts:      product_control

%description
This package contains the control file used for MicroOSNG installation.

%prep

%setup -n skelcd-control-MicroOSNG-%{version}

%build
make -C control

%check
make -C control check

%install
#
# Add control file 
#
mkdir -p $RPM_BUILD_ROOT/CD1

CONTROL_FILE=control.MicroOSNG.xml

install -m 644 control/$CONTROL_FILE $RPM_BUILD_ROOT/CD1/control.xml

%ifarch ppc ppc64
sed -i -e "s,http://download.opensuse.org/distribution/,http://download.opensuse.org/ports/ppc/distribution/," $RPM_BUILD_ROOT/CD1/control.xml
sed -i -e "s,http://download.opensuse.org/debug/,http://download.opensuse.org/ports/ppc/debug/," $RPM_BUILD_ROOT/CD1/control.xml
sed -i -e "s,http://download.opensuse.org/source/,http://download.opensuse.org/ports/ppc/source/," $RPM_BUILD_ROOT/CD1/control.xml
xmllint --noout --relaxng /usr/share/YaST2/control/control.rng $RPM_BUILD_ROOT/CD1/control.xml 
%endif

%files
%defattr(644,root,root,755)
%dir /CD1
/CD1/control.xml

%changelog
