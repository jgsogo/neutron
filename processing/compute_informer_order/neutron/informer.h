
#pragma once

#include <map>
#include "../utils/base_manager.h"
#include "types.h"

namespace neutron {
    class InformerManager : public ::utils::BaseManager<informer_id, region_id> {
        public:
            typedef std::map<informer_id, region_id> informer_container_type;
            typedef std::map<region_id, std::vector<informer_id>> informer_by_region_type;
            
        public:
            InformerManager(const std::string& filename);            
            const std::vector<informer_id>& get_by_region(const region_id& region);
            
        protected:
            informer_container_type _all;
            informer_by_region_type _all_by_region;
    };
}
