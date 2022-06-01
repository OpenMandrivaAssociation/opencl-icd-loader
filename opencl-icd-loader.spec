Name: opencl-icd-loader
Version: 2022.05.18
Release: 1
Source0: https://github.com/KhronosGroup/OpenCL-ICD-Loader/archive/refs/tags/v%{version}.tar.gz
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

%prep
%autosetup -p1 -n OpenCL-ICD-Loader-%{version}
%cmake -G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%check
cd build
LD_LIBRARY_PATH="`pwd`" ctest

%files -n %{libname}
%{_libdir}/libOpenCL.so.1*

%files -n %{devname}
%{_libdir}/libOpenCL.so
%{_datadir}/cmake/OpenCLICDLoader
