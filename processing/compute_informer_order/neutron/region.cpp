
#include <boost/filesystem.hpp>
#include "region.h"
#include "config_store.h"

namespace neutron {

    namespace {
        std::string regions_path() {
            namespace fs = boost::filesystem;
            auto regions_filename = ConfigStore::get().get_value_as<std::string>("files/regions");
            fs::path full_path = ConfigStore::get().get_value_as<std::string>("db_path") / fs::path(regions_filename);
            return full_path.string();
        }
    }

    RegionManager::RegionManager() : BaseManager<region_id, region_id, std::string>(regions_path()) {}

    Region::Region() {
    }

    Region::Region(const Region& other) : Region::BaseModel(other) {
    }

    Region::Region(const std::tuple<region_id, region_id, std::string>& data) : Region::BaseModel(data) {
    }

}
