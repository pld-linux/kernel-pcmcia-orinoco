#
# Conditional build:
# _without_dist_kernel	- without kernel from distribution
#
Summary:	Orinoco wireless cards driver
Summary(pl):	Sterownik kart bezprzewodowych Orinoco
Name:		kernel-pcmcia-orinoco
Version:	0.13d
%define	rel	0
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
URL:		http://airsnort.shmoo.com/orinocoinfo.html
Source0:	http://ozlabs.org/people/dgibson/dldwd/orinoco-%{version}.tar.gz
Patch1:		http://airsnort.shmoo.com/orinoco-0.13b-patched.diff
%{!?_without_dist_kernel:BuildRequires:	kernel-source}
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
ExclusiveArch:	%{ix86}
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Orinoco wireless cards driver. It contains patch to allow monitor mode
used by kismet.

%description -l pl
Sterownik kart bezprzewodowych Orinoco. Zawiera ³atkê umo¿liwaj±c±
u¿ycie trybu monitorowania wykorzystywanego przez kismet.

%package -n kernel-smp-pcmcia-orinoco
Summary:	Orinoco wireless cards SMP driver.
Summary(pl):	Sterownik SMP dla bezprzewodowych kart Orinoco.
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
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
%patch1 -p1

%build
%{__make} \
	KERNEL_VERSION=%{_kernel_ver} \
	KERNEL_SRC=%{_kernelsrcdir} \
	EXTRACFLAGS="-D__SMP__ -D_KERNEL_SMP=1"
mkdir smp
mv *.o smp/
%{__make} clean
%{__make} \
	KERNEL_VERSION=%{_kernel_ver} \
	KERNEL_SRC=%{_kernelsrcdir} \
	EXTRACFLAGS=""

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net/wireless/

install *.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/
install smp/*.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%postun
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%post	-n kernel-smp-pcmcia-orinoco
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp

%postun	-n kernel-smp-pcmcia-orinoco
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc README.orinoco
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*

%files -n kernel-smp-pcmcia-orinoco
%defattr(644,root,root,755)
%doc README.orinoco
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/*
