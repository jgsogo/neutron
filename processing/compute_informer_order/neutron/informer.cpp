
#include <boost/filesystem.hpp>

#include "informer.h"
#include "config_store.h"

namespace neutron {

    namespace {
        std::string informers_path() {
            namespace fs = boost::filesystem;
            fs::path full_path = ConfigStore::get().get_value_as<std::string>("db_path") / fs::path("informers.tsv");
            return full_path.string();
        }
    }

    InformerManager::InformerManager() : BaseManager<informer_id, region_id, float>(informers_path()) {
    }

    Informer::Informer() {
    }
    Informer::Informer(const std::tuple<informer_id, region_id, float>& data) : Informer::BaseModel(data) {
    }
}
