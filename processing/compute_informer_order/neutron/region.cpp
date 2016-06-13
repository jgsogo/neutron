
#include "region.h"
#include "queryset/read_file.h"

namespace neutron {
    RegionManager::RegionManager(const std::string& filename) {
        utils::read_file(filename, _data);
    }

    std::size_t RegionManager::count() const {
        return _data.size();
    }

}
