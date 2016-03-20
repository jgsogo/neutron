
#pragma once

#include "utils/base_manager.h"
#include "types.h"

namespace neutron {
    class InformerManager : public ::utils::BaseManager<informer_id, region_id> {
        public:
            typedef std::map<informer_id, region_id> informer_container_type;
            typedef std::map<region_id, std::vector<informer_id>> informer_by_region_type;
            
        public:
            InformerManager(const std::string& filename) : BaseManager(filename) {
                for(auto& item: _raw_data) {
                    const informer_id& first = std::get<0>(item);
                    const region_id& second = std::get<1>(item);
                    _all.insert(std::make_pair(first, second));
                    _all_by_region[second].push_back(first);
                }
            }
            
            const std::vector<informer_id>& get_by_region(const region_id& region) {
                informer_by_region_type::const_iterator it = _all_by_region.find(region);
                if (it != _all_by_region.end()) {
                    return it->second;
                }
                throw ::utils::NotFoundException("Region not found");
            }
            
        protected:
            informer_container_type _all;
            informer_by_region_type _all_by_region;
    };
}
