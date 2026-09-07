#ifndef CLUBPLATFORM_EXTENSION_API_H
#define CLUBPLATFORM_EXTENSION_API_H

#include <stdint.h>

#ifdef _WIN32
#  define CLUBPLATFORM_EXTENSION_EXPORT __declspec(dllexport)
#else
#  define CLUBPLATFORM_EXTENSION_EXPORT __attribute__((visibility("default")))
#endif

#ifdef __cplusplus
extern "C" {
#endif

#define CLUBPLATFORM_EXTENSION_ABI_VERSION 1u

typedef struct ClubPlatformHostApi {
    uint32_t abi_version;
    void (*log)(int level, const char* component, const char* message);
    int (*register_permission)(const char* id, const char* display_name);
    int (*register_menu_item)(const char* id, const char* parent_id, const char* label, const char* permission, const char* view_id);
    int (*register_view)(const char* id, const char* view_type, const char* resource);
    int (*register_rest_route)(const char* method, const char* path, const char* permission);
} ClubPlatformHostApi;

typedef struct ClubPlatformExtensionInfo {
    uint32_t abi_version;
    const char* id;
    const char* name;
    const char* version;
} ClubPlatformExtensionInfo;

typedef struct ClubPlatformExtensionHandle ClubPlatformExtensionHandle;

CLUBPLATFORM_EXTENSION_EXPORT ClubPlatformExtensionInfo clubplatform_extension_info(void);
CLUBPLATFORM_EXTENSION_EXPORT ClubPlatformExtensionHandle* clubplatform_extension_create(const ClubPlatformHostApi* host);
CLUBPLATFORM_EXTENSION_EXPORT int clubplatform_extension_start(ClubPlatformExtensionHandle* extension);
CLUBPLATFORM_EXTENSION_EXPORT void clubplatform_extension_stop(ClubPlatformExtensionHandle* extension);
CLUBPLATFORM_EXTENSION_EXPORT void clubplatform_extension_destroy(ClubPlatformExtensionHandle* extension);

#ifdef __cplusplus
}
#endif

#endif
