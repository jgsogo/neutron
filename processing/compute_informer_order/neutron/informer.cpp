
#include "informer.h"

namespace neutron {
    InformerManager::InformerManager(const std::string& filename) : BaseManager(filename) {
        for(auto& item: _raw_data) {
            const informer_id& first = std::get<0>(item);
            const region_id& second = std::get<1>(item);
            _all.insert(std::make_pair(first, second));
            _all_by_region[second].push_back(first);
        }
    }
            
    const std::vector<informer_id>& InformerManager::get_by_region(const region_id& region) {
        informer_by_region_type::const_iterator it = _all_by_region.find(region);
        if (it != _all_by_region.end()) {
            return it->second;
        }
        throw ::utils::NotFoundException("Region not found");
    }

}
