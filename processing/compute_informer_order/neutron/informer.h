
#pragma once

#include "utils/base_manager.h"

namespace neutron {
    class InformerManager : public utils::BaseManager<std::size_t, std::size_t> {
        public:
            typedef std::map<std::size_t, std::size_t> informer_container_type;
            typedef std::map<std::size_t, std::vector<std::size_t>> informer_by_region_type;
            
        public:
            InformerManager(const std::string& filename) : BaseManager(filename) {
                for(auto& item: _raw_data) {
                    const std::size_t& first = std::get<0>(item);
                    const std::size_t& second = std::get<1>(item);
                    _all.insert(std::make_pair(first, second));
                    _all_by_region[first].push_back(second);
                }
            }
        
            const std::vector<std::size_t>& get_by_region(const std::size_t& region) {
                informer_by_region_type::const_iterator it = _all_by_region.find(region);
                if (it != _all_by_region.end()) {
                    return it->second;
                }
                throw utils::NotFoundException("Region not found");
            }
        protected:
            informer_container_type _all;
            informer_by_region_type _all_by_region;
    };
}