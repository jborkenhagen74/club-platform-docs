#ifndef CLUBPLATFORM_EXTENSION_V3_H
#define CLUBPLATFORM_EXTENSION_V3_H
#include <clubplatform/extension_v2.h>
#ifdef __cplusplus
extern "C" {
#endif
/* Serialized calls. No exceptions, retained input pointers or external side
   effects. Output is plugin-owned UTF-8 JSON, valid until its next call and
   copied immediately by the host. No DB/STL/allocator crosses the ABI. */
enum ClubExtensionResultV3 { CLUB_V3_OK=1, CLUB_V3_REJECTED=0, CLUB_V3_ERROR=-1 };
typedef struct ClubExtensionV3 {
    uint32_t abi_version;
    uint32_t struct_size;
    const char* manifest_json;
    int (*validate)(const char* record_type,const char* values_json);
    int (*lifecycle)(const char* event,const char* context_json);
    const char* (*migrate_record)(uint32_t version,const char* record_type,const char* values_json);
    const char* (*invoke)(const char* capability,uint32_t version,const char* input_json);
} ClubExtensionV3;
typedef const ClubExtensionV3* (*ClubExtensionEntryV3)(void);
#ifdef __cplusplus
}
#endif
#endif
