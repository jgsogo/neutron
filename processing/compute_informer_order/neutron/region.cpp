
#include "region.h"

namespace neutron {
    /*
    class RegionManager::Impl {
        public:
            Impl(const std::string& filename) : _qs(filename) {};
            utils::FileQueryset<region_id, region_id, std::string> _qs;
    };

    RegionManager::RegionManager(const std::string& filename) : _impl(new Impl(filename)) {
    }

    RegionManager::~RegionManager() {
        delete _impl;
    }

    RegionManager::QuerySet RegionManager::all() const {
        return QuerySet(_impl->_qs);
    }
    */

    Region::Region() {
    }

    Region::Region(const std::tuple<region_id, region_id, std::string>& data) {
        _id = std::get<0>(data);
        _parent = std::get<1>(data);
        _name = std::get<2>(data);
    }

}
