#include <extension_v2.h>
#include <cstring>
#ifdef _WIN32
#include <windows.h>
#else
#include <dlfcn.h>
#endif
int main(int argc, char** argv) {
    if (argc != 2) return 1;
#ifdef _WIN32
    auto handle = LoadLibraryA(argv[1]);
    if (!handle) return 2;
    auto entry = reinterpret_cast<ClubExtensionEntryV2>(GetProcAddress(handle, "clubplatform_extension_v2"));
#else
    auto handle = dlopen(argv[1], RTLD_NOW | RTLD_LOCAL);
    if (!handle) return 2;
    auto entry = reinterpret_cast<ClubExtensionEntryV2>(dlsym(handle, "clubplatform_extension_v2"));
#endif
    if (!entry) return 3;
    const auto* module = entry();
    if (!module || module->abi_version != 2 || !module->manifest_json || !module->validate) return 4;
    if (!std::strstr(module->manifest_json, "attendance.session")) return 5;
    if (module != entry() || module->validate("attendance.session", "{}") != 1) return 6;
#ifdef _WIN32
    FreeLibrary(handle);
#else
    dlclose(handle);
#endif
    return 0;
}
