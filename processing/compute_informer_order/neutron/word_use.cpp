
#include "word_use.h"

#include <boost/filesystem.hpp>

#include "manager.h"
#include "config_store.h"


namespace neutron {

    namespace {
        std::string word_use_path() {
            namespace fs = boost::filesystem;
            auto word_use_filename = ConfigStore::get().get_value_as<std::string>("files/word_use");
            fs::path full_path = ConfigStore::get().get_value_as<std::string>("db_path") / fs::path(word_use_filename);
            return full_path.string();
        }
    }

    WordUseManager::WordUseManager() : BaseManager<WordUse>(word_use_path()) {}


    WordUse::WordUse() {
    }
    WordUse::WordUse(const BaseModel::tuple& data) : WordUse::BaseModel(data) {
    }

    WordUseManager& WordUse::objects() {
        static WordUseManager manager;
        return manager;
    }

}
