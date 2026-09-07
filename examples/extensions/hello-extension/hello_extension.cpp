#include "extension_api.h"

struct ClubPlatformExtensionHandle {
    const ClubPlatformHostApi* host;
};

extern "C" CLUBPLATFORM_EXTENSION_EXPORT ClubPlatformExtensionInfo clubplatform_extension_info(void) {
    return {CLUBPLATFORM_EXTENSION_ABI_VERSION, "example.hello", "Hello Extension", "0.1.0"};
}

extern "C" CLUBPLATFORM_EXTENSION_EXPORT ClubPlatformExtensionHandle* clubplatform_extension_create(const ClubPlatformHostApi* host) {
    if (host == nullptr || host->abi_version != CLUBPLATFORM_EXTENSION_ABI_VERSION) {
        return nullptr;
    }
    return new ClubPlatformExtensionHandle{host};
}

extern "C" CLUBPLATFORM_EXTENSION_EXPORT int clubplatform_extension_start(ClubPlatformExtensionHandle* extension) {
    if (extension == nullptr) {
        return -1;
    }
    extension->host->register_permission("example.hello.read", "Read Hello Extension");
    extension->host->register_view("example.hello.view", "qml", "qrc:/example/Hello.qml");
    extension->host->register_menu_item("example.hello.menu", "main.extensions", "Hello", "example.hello.read", "example.hello.view");
    extension->host->log(1, "example.hello", "Hello Extension started");
    return 0;
}

extern "C" CLUBPLATFORM_EXTENSION_EXPORT void clubplatform_extension_stop(ClubPlatformExtensionHandle* extension) {
    if (extension != nullptr) {
        extension->host->log(1, "example.hello", "Hello Extension stopped");
    }
}

extern "C" CLUBPLATFORM_EXTENSION_EXPORT void clubplatform_extension_destroy(ClubPlatformExtensionHandle* extension) {
    delete extension;
}
