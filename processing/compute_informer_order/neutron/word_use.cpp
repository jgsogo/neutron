
#include "word_use.h"

#include <boost/filesystem.hpp>

#include "manager.h"
#include "config_store.h"


namespace neutron {

    namespace {
        std::string word_use_path() {
            namespace fs = boost::filesystem;
            auto word_use_filename = ConfigStore::get().get_value_as<std::string>("files/worduse_data");
            fs::path full_path = ConfigStore::get().get_value_as<std::string>("db_path") / fs::path(word_use_filename);
            return full_path.string();
        }
    }

    WordUseManager::WordUseManager() : BaseManager<WordUse>(word_use_path()) {}


    std::ostream& operator << (std::ostream& os, const WordUseChoices& w) {
        switch(w._choices) {
            case WordUseChoices::OK: return os << "Ok";
            case WordUseChoices::NOT_ME: return os << "Not me";
            case WordUseChoices::UNKNOWN: return os << "Unknown";
            case WordUseChoices::UNRECOGNIZED: return os << "Unrecognized";
            default: return os << "None(" << w._choices << ")";
        }
    }



    WordUse::WordUse() {
    }
    WordUse::WordUse(const BaseModel::tuple& data) : WordUse::BaseModel(data) {
    }

    WordUseManager& WordUse::objects() {
        static WordUseManager manager;
        return manager;
    }

}
