#include <clubplatform/extension_v3.h>
#include <nlohmann/json.hpp>
#include <string>
using nlohmann::json;
#ifndef V3_FIXTURE
#define V3_FIXTURE 0
#endif
namespace {
std::string declaration() {
    json m={{"id","sample"},{"name_key","module.sample.name"},{"version","1.0.0"},{"abi",3},{"core",{{"minimum","1.0.0"},{"maximum_exclusive","2.0.0"}}},
        {"accepts_v2",true},{"schema_version",1},{"migrations",json::array({{{"version",1},{"definition","Initial sample note records"}}})},
        {"permissions",{"sample.read","sample.write","sample.archive","sample.restore","sample.delete"}},
        {"capabilities",json::array({{{"key","document.placeholder-provider"},{"version",1}},{{"key","record.references"},{"version",1}}})},
        {"types",json::array({{{"key","sample.note"},{"label","Sample note"},{"label_key","module.sample.note"},{"fields",json::array({{{"key","text"},{"label","Text"},{"label_key","module.sample.text"},{"type","text"},{"required",true}}})}}})},
        {"placeholders",json::array({{{"key","sample.note.text"},{"label_key","placeholder.sample.note.text.label"},{"description_key","placeholder.sample.note.text.description"},{"scope","person"},{"source","extension"},{"value_type","text"},{"required_permission","sample.read"},{"record_type","sample.note"}}})}};
    if(V3_FIXTURE==1 || V3_FIXTURE==2) {m["version"]="1.1.0";m["schema_version"]=2;m["migrations"].push_back({{"version",2},{"definition","Add category without discarding text"}});m["types"][0]["fields"].push_back({{"key","category"},{"label","Category"},{"type","text"},{"required",true}});}
    if(V3_FIXTURE==4) m["dependencies"]=json::array({{{"id","missing"},{"minimum","1.0.0"}}});
    if(V3_FIXTURE==5) m["dependencies"]=json::array({{{"id","sample"},{"minimum","1.0.0"}}});
    if(V3_FIXTURE==6) m["core"]["minimum"]="99.0.0";
    if(V3_FIXTURE==7) m["capabilities"][0]["version"]=9;
    if(V3_FIXTURE==8) m={{"id","sample"},{"name","Sample legacy"},{"version","0.9.0"},{"types",m["types"]}};
    return m.dump();
}
int validate(const char*,const char* data) noexcept {try {const auto v=json::parse(data);return v.at("text").is_string() && !v.at("text").get<std::string>().empty()?CLUB_V3_OK:CLUB_V3_REJECTED;}catch(...) {return CLUB_V3_ERROR;}}
int lifecycle(const char*,const char*) noexcept {return CLUB_V3_OK;}
const char* migrate(uint32_t version,const char*,const char* data) noexcept {
    try {static std::string output;auto v=json::parse(data);if(version==2) {if(V3_FIXTURE==2) return nullptr;v["category"]="general";}output=v.dump();return output.c_str();}catch(...) {return nullptr;}
}
const char* invoke(const char* capability,uint32_t version,const char* input) noexcept {
    if(version!=1) return nullptr;
    try {static std::string output;const auto data=json::parse(input);
        if(std::string(capability)=="record.references") {bool referenced=false;for(const auto& e:data.at("entries")) if(e.at("owner_id")==data.at("entity_id")) referenced=true;output=json{{"referenced",referenced}}.dump();}
        else if(std::string(capability)=="document.placeholder-provider") output=json{{"value",data.at("records").at(0).at("values").at("text")}}.dump();
        else return nullptr;
        return output.c_str();
    }catch(...) {return nullptr;}
}
const auto manifest=declaration();
const ClubExtensionV3 api{3,V3_FIXTURE==3?8u:static_cast<uint32_t>(sizeof(ClubExtensionV3)),manifest.c_str(),validate,lifecycle,migrate,invoke};
const ClubExtensionV2 legacy{2,manifest.c_str(),validate};
}
#if V3_FIXTURE==8
extern "C" CLUB_EXTENSION_EXPORT const ClubExtensionV2* clubplatform_extension_v2() {return &legacy;}
#else
extern "C" CLUB_EXTENSION_EXPORT const ClubExtensionV3* clubplatform_extension_v3() {return &api;}
#endif
