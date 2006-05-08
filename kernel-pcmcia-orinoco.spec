#
# Conditional build:
%bcond_without	dist_kernel     # allow non-distribution kernel
%bcond_without	kernel          # don't build kernel modules
%bcond_without	smp             # don't build SMP module
%bcond_with	verbose         # verbose build (V=1)
#
Summary:	Orinoco wireless cards driver
Summary(pl):	Sterownik kart bezprzewodowych Orinoco
Name:		kernel-pcmcia-orinoco
Version:	0.15rc4
%define	rel	0
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/orinoco/orinoco-%{version}.tar.gz
# Source0-md5:	bf7de689b98fb0f0f821df95b355997e
URL:		http://airsnort.shmoo.com/orinocoinfo.html
%{?with_dist_kernel:BuildRequires:	kernel-source >= 2.6.0}
BuildRequires:	rpmbuild(macros) >= 1.118
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Orinoco wireless cards driver. It contains patch to allow monitor mode
used by kismet.

%description -l pl
Sterownik kart bezprzewodowych Orinoco. Zawiera ³atkê umo¿liwiaj±c±
u¿ycie trybu monitorowania wykorzystywanego przez kismet.

%package -n kernel-smp-pcmcia-orinoco
Summary:	Orinoco wireless cards SMP driver.
Summary(pl):	Sterownik SMP dla bezprzewodowych kart Orinoco.
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-pcmcia-orinoco
Orinoco wireless cards driver. It contains patch to allow monitor mode
used by kismet. SMP version.

%description -n kernel-smp-pcmcia-orinoco -l pl
Sterownik kart bezprzewodowych Orinoco. Zawiera ³atkê umo¿liwaj±c±
u¿ycie trybu monitorowania wykorzystywanego przez kismet. Wersja dla
j±der wieloprocesorowych.

%prep
%setup -q -n orinoco-%{version}

%build
%if %{with kernel}
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
    install -d $cfg
    if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
        exit 1
    fi
    rm -rf include
    install -d include/{linux,config}
    ln -sf %{_kernelsrcdir}/config-$cfg .config
    ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
    ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
    ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
    touch include/config/MARKER
#    ln -sf %{_kernelsrcdir}/scripts scripts
#
#       patching/creating makefile(s) (optional)
#
    %{__make} -C %{_kernelsrcdir} clean \
        RCS_FIND_IGNORE="-name '*.ko' -o" \
        M=$PWD O=$PWD \
        %{?with_verbose:V=1}
    %{__make} -C %{_kernelsrcdir} modules \
        CC="%{__cc}" CPP="%{__cpp}" \
        M=$PWD O=$PWD \
        %{?with_verbose:V=1}

    mv *.ko $cfg
done
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net/wireless

%if %{with kernel}
install %{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}/*.ko \
        $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless
%if %{with smp} && %{with dist_kernel}
install smp/*.ko \
        $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-pcmcia-orinoco
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-pcmcia-orinoco
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files
%defattr(644,root,root,755)
%doc README.orinoco
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-pcmcia-orinoco
%defattr(644,root,root,755)
%doc README.orinoco
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/*
%endif
%endif
