
#include <boost/filesystem.hpp>
#include "region.h"
#include "config_store.h"

namespace neutron {

    namespace {
        std::string regions_path() {
            namespace fs = boost::filesystem;
            fs::path full_path = ConfigStore::get().get_value_as<std::string>("db_path") / fs::path("regions.tsv");
            return full_path.string();
        }
    }

    RegionManager::RegionManager() : BaseManager<region_id, region_id, std::string>(regions_path()) {}

    Region::Region() {
    }
    Region::Region(const std::tuple<region_id, region_id, std::string>& data) : Region::BaseModel(data) {
    }

}
