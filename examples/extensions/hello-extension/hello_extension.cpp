#include <extension_v2.h>

namespace {
// The host validates all declared types, required fields and dates first.
// This example has no extra business constraint and needs no private Core code.
int validate(const char*, const char*) noexcept { return 1; }
const ClubExtensionV2 extension{
    2,
    R"({"id":"attendance","name":"Attendance","version":"1.0.0","types":[{"key":"attendance.session","label":"Training attendance","fields":[{"key":"attended_on","label":"Date","type":"date"},{"key":"course","label":"Course","type":"text"}]}]})",
    validate
};
}

extern "C" CLUB_EXTENSION_EXPORT const ClubExtensionV2* clubplatform_extension_v2(void) {
    return &extension;
}
