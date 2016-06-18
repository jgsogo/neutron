
#include "config_store.h"
#include "rapidjson/document.h"
#include <rapidjson/filereadstream.h>

namespace neutron {

    struct ConfigStore::Data {
        rapidjson::Document d;

    };


    ConfigStore::ConfigStore() : _data(new Data) {}
    ConfigStore::~ConfigStore() {
        delete _data;
    }

    ConfigStore& ConfigStore::get() {
        static ConfigStore instance;
        return instance;
    }

    void ConfigStore::parse_data(const std::string& data) {
        _data->d.Parse(data.c_str());
    }

    void ConfigStore::parse_file(const std::string& filename) {
        FILE* pFile = fopen(filename.c_str(), "rb");
        char buffer[65536];
        rapidjson::FileReadStream is(pFile, buffer, sizeof(buffer));
        _data->d.ParseStream(is);
    }

    std::string ConfigStore::get_value(const std::string& key) const {
        return _data->d[key.c_str()].GetString();
    }

    bool ConfigStore::has_value(const std::string& key) const {
        return _data->d.HasMember(key.c_str());
    }
}
