
#include "config_store.h"
#include <vector>
#include <sstream>
#include <stdexcept>

#include "rapidjson/document.h"
#include "rapidjson/filereadstream.h"
#include "rapidjson/error/en.h"

namespace neutron {

    namespace {
        std::vector<std::string> &split(const std::string &s, char delim, std::vector<std::string> &elems) {
            std::stringstream ss(s);
            std::string item;
            while (std::getline(ss, item, delim)) {
                elems.push_back(item);
            }
            return elems;
        }

        std::vector<std::string> split(const std::string &s, char delim) {
            std::vector<std::string> elems;
            split(s, delim, elems);
            return elems;
        }
    }


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
        // TODO: http://rapidjson.org/md_doc_stream.html#IStreamWrapper v1.0.3
        _data->d.Parse(data.c_str());
    }

    void ConfigStore::parse_file(const std::string& filename) {
        FILE* pFile = fopen(filename.c_str(), "rb");
        char buffer[65536];
        rapidjson::FileReadStream is(pFile, buffer, sizeof(buffer));
        _data->d.ParseStream(is);
        if (_data->d.HasParseError()) {
            std::stringstream os; os << "Parse error '";
            os << rapidjson::GetParseError_En(_data->d.GetParseError());
            os << "' at position " << _data->d.GetErrorOffset() << ".";
            throw std::runtime_error(os.str());
        }
    }

    std::string ConfigStore::get_value(const std::string& key) const {
        auto tokens = split(key, '/');
        auto it_token = tokens.begin();
        auto member = _data->d.FindMember((*it_token).c_str());
        while (++it_token != tokens.end()) {
            member = member->value.FindMember((*it_token).c_str());
        }
        return member->value.GetString();
    }

    bool ConfigStore::has_value(const std::string& key) const {
        return _data->d.HasMember(key.c_str());
    }
}
