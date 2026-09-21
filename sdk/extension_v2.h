#ifndef CLUBPLATFORM_EXTENSION_V2_H
#define CLUBPLATFORM_EXTENSION_V2_H
#include <stdint.h>
#ifdef _WIN32
#define CLUB_EXTENSION_EXPORT __declspec(dllexport)
#else
#define CLUB_EXTENSION_EXPORT __attribute__((visibility("default")))
#endif
#ifdef __cplusplus
extern "C" {
#endif
/* No allocator, STL object or database handle crosses the ABI boundary.
   Strings stay plugin-owned; validators must not throw and return 1 on success. */
typedef struct ClubExtensionV2 {
    uint32_t abi_version;
    const char* manifest_json;
    int (*validate)(const char* record_type, const char* values_json);
} ClubExtensionV2;
/* The module exports clubplatform_extension_v2 with CLUB_EXTENSION_EXPORT.
   Consumers resolve this entry dynamically; no DLL export declaration in the host. */
typedef const ClubExtensionV2* (*ClubExtensionEntryV2)(void);
#ifdef __cplusplus
}
#endif
#endif
