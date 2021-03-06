
#include "informer.h"

#include <boost/filesystem.hpp>

#include "manager.h"
#include "config_store.h"


namespace neutron {

    namespace {
        std::string informers_path() {
            namespace fs = boost::filesystem;
            auto informers_filename = ConfigStore::get().get_value_as<std::string>("files/informers_data");
            fs::path full_path = ConfigStore::get().get_value_as<std::string>("db_path") / fs::path(informers_filename);
            return full_path.string();
        }
    }

    InformerManager::InformerManager() : BaseManager<Informer>(informers_path()) {}
    

    Informer::Informer() {
    }

    Informer::Informer(const informer_id& id) {
        std::get<0>(_data) = id;
    }

    Informer::Informer(const std::tuple<informer_id, Region, float>& data) : Informer::BaseModel(data) {
    }

    InformerManager& Informer::objects() {
        static InformerManager manager;
        return manager;
    }

    const float Informer::get_confidence() const {
        return std::get<2>(_data);
    }
}
