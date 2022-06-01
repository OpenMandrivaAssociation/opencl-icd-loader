%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

Name: opencl-icd-loader
Version: 2022.05.18
Release: 1
Source0: https://github.com/KhronosGroup/OpenCL-ICD-Loader/archive/refs/tags/v%{version}.tar.gz
# For compatibility with ocl-icd
Source1: OpenCL.pc.in
Summary: OpenCL ICD Loader - a wrapper to load different OpenCL implementations
URL: https://github.com/opencl-icd-loader/opencl-icd-loader
License: Apache-2.0
Group: System/Libraries
BuildRequires: cmake(OpenCLHeaders)
BuildRequires: cmake ninja

%description
OpenCL defines an Installable Client Driver (ICD) mechanism to allow developers
to build applications against an Installable Client Driver loader (ICD loader)
rather than linking their applications against a specific OpenCL
implementation. The ICD Loader is responsible for:

* Exporting OpenCL API entry points
* Enumerating OpenCL implementations
* Forwarding OpenCL API calls to the correct implementation

%define libname %mklibname OpenCL
%define devname %mklibname -d OpenCL

%package -n %{libname}
Summary: OpenCL ICD Loader library
Group: System/Libraries

%description -n %{libname}
OpenCL ICD Loader library

%package -n %{devname}
Summary: Development files for the OpenCL ICD Loader
Group: Development/Libraries
Requires: %{libname} = %{EVRD}
Requires: cmake(OpenCLHeaders)

%description -n %{devname}
Development files for the OpenCL ICD Loader

%if %{with compat32}
%define lib32name libOpenCL
%define dev32name libOpenCL-devel

%package -n %{lib32name}
Summary: 32-bit OpenCL ICD Loader library
Group: System/Libraries

%description -n %{lib32name}
32-bit OpenCL ICD Loader library

%package -n %{dev32name}
Summary: 32-bit Development files for the OpenCL ICD Loader
Group: Development/Libraries
Requires: %{lib32name} = %{EVRD}
Requires: %{devname} = %{EVRD}
Requires: cmake(OpenCLHeaders)

%description -n %{dev32name}
32-bit Development files for the OpenCL ICD Loader
%endif

%prep
%autosetup -p1 -n OpenCL-ICD-Loader-%{version}
%cmake -G Ninja

%if %{with compat32}
cd ..
TOP="$(pwd)"
cat >xc <<EOF
exec %{_bindir}/clang -rtlib=compiler-rt -m32 "\$@"
EOF
chmod +x xc
cat >cmake-i686.toolchain <<EOF
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR i686)
set(CMAKE_C_COMPILER ${TOP}/xc)
set(CMAKE_CXX_COMPILER ${TOP}/xc++)
EOF
CFLAGS="$(echo %{optflags} |sed -e 's,m64,m32,g')" LDFLAGS="$(echo %{optflags} |sed -e 's,m64,m32,g')" %cmake32 \
	-DCMAKE_TOOLCHAIN_FILE=${TOP}/cmake-i686.toolchain \
	-G Ninja
%endif

%build
%ninja_build -C build
%if %{with compat32}
%ninja_build -C build32
%endif

%install
%if %{with compat32}
%ninja_install -C build32
mkdir -p %{buildroot}%{_prefix}/lib/pkgconfig
sed -e 's,@prefix@,%{_prefix},g;s,@exec_prefix@,%{_prefix},g;s,@libdir@,%{_prefix}/lib,g;s,@includedir@,%{_includedir},g;s,@OPENCL_VERSION@,3.0,' %{S:1} >%{buildroot}%{_prefix}/lib/pkgconfig/OpenCL.pc
%endif
%ninja_install -C build
mkdir -p %{buildroot}%{_libdir}/pkgconfig
sed -e 's,@prefix@,%{_prefix},g;s,@exec_prefix@,%{_prefix},g;s,@libdir@,%{_libdir},g;s,@includedir@,%{_includedir},g;s,@OPENCL_VERSION@,3.0,' %{S:1} >%{buildroot}%{_libdir}/pkgconfig/OpenCL.pc

%check
cd build
LD_LIBRARY_PATH="`pwd`" ctest
%if %{with compat32}
cd ../build32
LD_LIBRARY_PATH="`pwd`" ctest
%endif

%files -n %{libname}
%{_libdir}/libOpenCL.so.1*

%files -n %{devname}
%{_libdir}/libOpenCL.so
%{_datadir}/cmake/OpenCLICDLoader
%{_libdir}/pkgconfig/OpenCL.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libOpenCL.so.1*

%files -n %{dev32name}
%{_prefix}/lib/libOpenCL.so
%{_prefix}/lib/pkgconfig/OpenCL.pc
%endif
